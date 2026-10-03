import os
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from backend.clinic_state import ClinicState

def run_agent(conversation_id: str, today: str, turns: list[str]) -> dict:
    start_time = time.monotonic()
    state = ClinicState()
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    tool_calls_record = []
    context = {
        "terminal_state": "abandoned",
        "escalation_reason": None,
        "patient_id": None,
        "appointment_id": None,
        "reply": ""
    }
    
    # [Tool definitions exactly as before...]
    def search_slots(doctor_id: str, date: str) -> list[str]:
        try:
            return state.search_slots(doctor_id, date)
        except Exception as e:
            return {"error": str(e)}

    def book_appointment(caller_id: str, patient_id: str, doctor_id: str, date: str, start: str) -> dict:
        try:
            res = state.book_appointment(caller_id, patient_id, doctor_id, date, start)
            context["terminal_state"] = "booked"
            context["patient_id"] = patient_id
            context["appointment_id"] = res["id"]
            return res
        except Exception as e:
            if "not authorized" in str(e).lower():
                return {"error": str(e), "hint": "You MUST call escalate_to_human with reason 'not_authorised' now."}
            return {"error": str(e)}

    def reschedule_appointment(caller_id: str, appointment_id: str, date: str, start: str) -> dict:
        try:
            res = state.reschedule_appointment(caller_id, appointment_id, date, start)
            context["terminal_state"] = "rescheduled"
            context["appointment_id"] = appointment_id
            context["patient_id"] = res["patient_id"]
            return res
        except Exception as e:
            if "not authorized" in str(e).lower():
                return {"error": str(e), "hint": "You MUST call escalate_to_human with reason 'not_authorised' now."}
            return {"error": str(e)}

    def cancel_appointment(caller_id: str, appointment_id: str) -> dict:
        try:
            res = state.cancel_appointment(caller_id, appointment_id)
            context["terminal_state"] = "cancelled"
            context["appointment_id"] = appointment_id
            context["patient_id"] = res["patient_id"]
            return res
        except Exception as e:
            if "not authorized" in str(e).lower():
                return {"error": str(e), "hint": "You MUST call escalate_to_human with reason 'not_authorised' now."}
            return {"error": str(e)}

    def lookup_patient(search_term: str) -> list[dict]:
        try:
            return state.lookup_patient(search_term)
        except Exception as e:
            return {"error": str(e)}

    def escalate_to_human(reason: str) -> dict:
        valid_reasons = ['clinical_urgent', 'medical_advice', 'not_authorised', 'ambiguous_patient', 'out_of_scope']
        if reason not in valid_reasons:
            return {"error": f"Invalid reason. Must be one of {valid_reasons}"}
        
        context["terminal_state"] = "escalated"
        context["escalation_reason"] = reason
        return {"status": "escalated", "reason": reason}

    tools_list = [search_slots, book_appointment, reschedule_appointment, cancel_appointment, lookup_patient, escalate_to_human]
    
    system_instruction = f"""You are a clinic front desk agent for Sunrise Clinic in Dehradun.
Today's date is {today}.

CRITICAL RULES:
1. DO NOT HALLUCINATE: You must use tools to look up patients, check slots, and book/cancel. NEVER invent a slot, patient, or appointment that a tool did not return.
2. AUTHORIZATION: The mutating tools require `caller_id` and `patient_id`. The caller is the person on the phone. The patient is who the appointment is for. If the tool returns an authorization error, you MUST immediately call `escalate_to_human(reason='not_authorised')`.
3. AMBIGUOUS PATIENT: If lookup_patient returns multiple matches and the user says "just pick one" or doesn't clarify, DO NOT guess. Call `escalate_to_human(reason='ambiguous_patient')`.
4. MEDICAL EMERGENCY (HARD RULE): If a caller reports symptoms that need a clinician now (e.g. chest pain, active bleeding, severe pain), STOP booking and immediately call `escalate_to_human(reason='clinical_urgent')`.
5. MEDICAL ADVICE: If a caller asks if they should take a medicine or see a doctor, call `escalate_to_human(reason='medical_advice')`.
6. OUT OF SCOPE / IMPOSSIBLE: If they ask to book in the past, or ask for a doctor that doesn't exist, politely decline and end the conversation (this will default to 'abandoned' or 'refused' which is correct).
7. ONLY one final text response after your tool calls are done.
"""

    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools_list,
            temperature=0.0
        )
    )

    def resilient_send(payload):
        """Send message with 429 rate limit backoff."""
        max_retries = 5
        for attempt in range(max_retries):
            try:
                return chat.send_message(payload)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print(f"Rate limit hit. Retrying in 30 seconds... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(30)
                else:
                    raise e
        raise Exception("Max retries exceeded for rate limit.")

    tokens = 0
    # Process turns
    for turn in turns:
        try:
            response = resilient_send(turn)
            if response.usage_metadata:
                tokens += response.usage_metadata.total_token_count
                
            while response.function_calls:
                parts = []
                for fc in response.function_calls:
                    tool_calls_record.append({
                        "name": fc.name,
                        "arguments": fc.args
                    })
                    
                    if fc.name == "search_slots":
                        res = search_slots(**fc.args)
                    elif fc.name == "book_appointment":
                        res = book_appointment(**fc.args)
                    elif fc.name == "reschedule_appointment":
                        res = reschedule_appointment(**fc.args)
                    elif fc.name == "cancel_appointment":
                        res = cancel_appointment(**fc.args)
                    elif fc.name == "lookup_patient":
                        res = lookup_patient(**fc.args)
                    elif fc.name == "escalate_to_human":
                        res = escalate_to_human(**fc.args)
                    else:
                        res = {"error": "Unknown tool"}
                        
                    parts.append(types.Part.from_function_response(
                        name=fc.name,
                        response={"result": res}
                    ))
                
                response = resilient_send(parts)
                if response.usage_metadata:
                    tokens += response.usage_metadata.total_token_count
                
            context["reply"] = response.text
        except Exception as e:
            print(f"Error calling LLM: {e}")
            if context["terminal_state"] == "abandoned":
                context["terminal_state"] = "refused"
            context["reply"] = "I am sorry, I encountered an internal error."

    elapsed_ms = int((time.monotonic() - start_time) * 1000)
    
    return {
        "conversation_id": conversation_id,
        "tool_calls": tool_calls_record,
        "terminal_state": context["terminal_state"],
        "escalation_reason": context["escalation_reason"],
        "patient_id": context["patient_id"],
        "appointment_id": context["appointment_id"],
        "reply": context["reply"] or "",
        "metrics": {
            "turns": len(turns),
            "tokens": tokens,
            "latency_ms": elapsed_ms
        }
    }
