import os
from google import genai
from google.genai import types
from pydantic import BaseModel

def test_genai():
    client = genai.Client()
    
    def search_slots(doctor_id: str, date: str) -> list[str]:
        """Search available slots for a doctor on a specific date."""
        return ["09:00", "09:15"]

    model = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='When is dr_rao available on 2026-10-01?',
        config=types.GenerateContentConfig(
            tools=[search_slots],
            temperature=0.0
        )
    )
    print(model.function_calls)

if __name__ == "__main__":
    test_genai()
