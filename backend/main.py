from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from backend.agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In a real production scenario, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    conversation_id: str
    today: str
    turns: List[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/agent/run")
def agent_run(req: RunRequest):
    try:
        result = run_agent(req.conversation_id, req.today, req.turns)
        return result
    except Exception as e:
        print(f"Error in agent_run: {e}")
        return {
            "conversation_id": req.conversation_id,
            "tool_calls": [],
            "terminal_state": "refused",
            "escalation_reason": None,
            "patient_id": None,
            "appointment_id": None,
            "reply": "An internal error occurred.",
            "metrics": {"turns": len(req.turns), "tokens": 0, "latency_ms": 0}
        }
