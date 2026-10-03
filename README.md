# SwasthiQ Clinic Front Desk Agent

## Overview
A Python REST API exposing a conversational agent backed by Gemini 2.5 Flash, alongside a React frontend matching the exact SwasthiQ Handoff Queue and Conversation Detail screens.

## Architecture
The key design decision was separating the untrusted LLM from the mutation layer. The LLM acts purely as a decision-maker proposing operations, but `ClinicState` (the tool layer) acts as the absolute ground truth. It validates every argument, authorization boundary, slot, and mutation.

## Safety Model
- **Zero Hallucination:** The tool layer tracks `revealed_slots` and outright rejects attempts to book slots that were never queried.
- **Emergencies:** The prompt strictly enforces escalation (`clinical_urgent`) the moment medical distress is detected, terminating booking operations.
- **Authorization:** Handled exclusively inside the tool layer using guardian mapping.

## API Contract

### POST /agent/run
Accepts `{ "conversation_id": "...", "today": "...", "turns": [...] }` and returns the exact schema specified in `schema.md`.

## Six Tools
1. `search_slots`
2. `book_appointment` (Enforces `caller_id` authorization)
3. `reschedule_appointment` (Enforces `caller_id` authorization)
4. `cancel_appointment` (Enforces `caller_id` authorization)
5. `lookup_patient`
6. `escalate_to_human` (Accepts discrete reasons like `clinical_urgent`)

## State Consistency
`clinic.json` state is completely isolated and resets per API request.

## Determinism & API Resilience
- **Agent Determinism**: The same conversation produced the same terminal state across repeated runs in the automated harness. (cv_0011 was successfully validated across 3 runs with deterministic `escalated/clinical_urgent` results).
- **API Resilience**: Transient Gemini 429 quota exhaustion errors are handled with an automatic retry/backoff mechanism in the backend.

## Model & Performance
- **Model:** gemini-2.5-flash
- **Tokens/Conversation:** ~2,500 - 4,500
- **Latency/Conversation:** ~3 - 5 seconds

## Running Locally

1. **Backend**:
   ```bash
   set GEMINI_API_KEY=your_key
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --port 8000
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Running Tests
Run the deterministic harness suite:
```bash
python runner.py --url http://localhost:8000/agent/run --repeat 3
```
Run the tool layer validation suite (verifies mutation/auth without LLM):
```bash
python backend/test_tool_layer.py
```

## Adversarial Cases
Included in `/adversarial/`. Designed to explicitly test prompt injection, unauthorized booking, ambiguous patients, nonexistent slots, hidden emergencies, and double-booking.

## Deployment
- **Frontend**: [Link to Vercel/Netlify]
- **Backend**: [Link to Render/Fly.io]
- **Video**: [Link to Loom]
