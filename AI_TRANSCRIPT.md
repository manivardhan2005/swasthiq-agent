# AI Transcript

## Initial Request
The user provided the `swasthiq-front-desk-agent-starter-pack.zip` and the PDF instructions, asking to build a Python REST API conversational agent with six tools and a React frontend matching two specific screens.

## Agent Approach
1. **File Ingestion**: The AI read the `README.md`, `schema.md`, `clinic.json`, and `runner.py` to understand the constraints. State isolation and deterministic output were prioritized.
2. **Backend Setup**: The AI wrote the `clinic_state.py` containing the logic for the six tools.
3. **Agent Logic**: The AI used `google-genai` (Gemini 2.5 Flash) to orchestrate the LLM, setting up strict system instructions to enforce authorization, avoid hallucination, and respect the "One Hard Rule" (medical emergencies).
4. **Tool Invariants**: The AI implemented strict invariants inside `ClinicState` (tracking `revealed_slots` and `revealed_patients`) to ensure the LLM could never force an un-searched slot or guess an ambiguous patient.
5. **Testing & Validation**: The AI wrote a Python unit test (`test_tool_layer.py`) to verify concurrency, authorization, and mutation locks independent of the LLM. The AI then handled a rate-limit issue (429) by implementing a robust retry/backoff mechanism in the LLM calls.
6. **Frontend Development**: The AI set up a Vite + React + TailwindCSS frontend, precisely matching the Handoff Queue and Conversation Detail screens with static data.
7. **Documentation**: The AI generated 8 robust adversarial scripts, the `README.md`, and the `DECISIONS.md`.

## Final Verification
The AI confirmed that the tool layer physically rejected hallucinations and that `cv_0011` explicitly triggered the `clinical_urgent` escalation across 3 deterministic runs, as verified by the user executing the test harness locally.
