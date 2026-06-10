import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_ticket(text: str):
    prompt = f"""
    You are a university IT/helpdesk assistant.

    Return STRICT JSON only.

    Keep responses SHORT and professional.

    Schema:
    {{
      "response": "2-3 line helpful reply",
      "category": "Academic / Finance / IT / Hostel / Other",
      "department": "handling department",
      "urgency": "Low | Medium | High",
      "db_summary": "internal short issue note",
      "faculty_action": "one-line fix instruction"
    }}

    Student issue:
    {text}
    """

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    raw = response.text.strip()

    try:
        return json.loads(raw)
    except Exception:
        # fallback safety (VERY IMPORTANT)
        return {
            "response": "Sorry, I couldn't process your request properly.",
            "category": "Other",
            "department": "General",
            "urgency": "Medium",
            "db_summary": raw[:200],
            "faculty_action": "Review manually"
        }