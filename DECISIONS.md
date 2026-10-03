# Decisions and Ambiguities

## Why the tool layer owns mutations
The LLM proposes actions but cannot establish facts or mutate clinic state directly. All mutations pass through `ClinicState`. 
This prevents an LLM-generated appointment ID, patient ID, or slot from becoming authoritative. By maintaining `revealed_slots` and `revealed_patients` trackers, the tool physically rejects any attempt to book a slot or use a patient ID that was not previously returned by a tool call.

## Why ambiguous patients escalate
Selecting one candidate from multiple matches would require the model to guess identity. The tool therefore returns all candidates, and the prompt instructs the agent to either clarify or escalate via `ambiguous_patient`.

## Why emergency detection terminates the flow
A clinical emergency takes precedence over administrative work (the "One Hard Rule"). Once identified, no further booking/rescheduling/cancellation tool is permitted. The LLM immediately halts and emits `escalate_to_human('clinical_urgent')`.

## State Isolation
The `clinic.json` file is reloaded on every single POST request to `/agent/run`. This ensures full compliance with the requirement that state resets between conversations.

## Authorization
Because the tool layer is the ground truth, mutating tools (`book_appointment`, etc.) explicitly require a `caller_id` and `patient_id`. The tool layer verifies the caller is either the target patient or their registered guardian. If unauthorized, the tool raises a specific error commanding the LLM to call `escalate_to_human(reason='not_authorised')`.

## Concurrency
Explicit lock-like checks are performed in `clinic_state.py` just before mutation. Any double-booking attempts natively throw errors.

## Model Output Reliability
I used `google-genai` and `gemini-2.5-flash`. The model's function calling guarantees structural validity. Any arbitrary SDK crashes or prompt injections are caught by a global exception handler in the FastAPI endpoint, safely returning a fallback `schema.md` compliant response with `terminal_state: "refused"`.
