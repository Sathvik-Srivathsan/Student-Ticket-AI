from fastapi import FastAPI
from pydantic import BaseModel
import json

from backend.llm_service import analyze_ticket
from db.supabase_client import supabase

app = FastAPI()

class Ticket(BaseModel):
    text: str


@app.post("/create-ticket")
def create_ticket(ticket: Ticket):

    try:
        result = analyze_ticket(ticket.text)

        # extra safety (in case llm returns string)
        if isinstance(result, str):
            result = json.loads(result)

        data = {
            "user_text": ticket.text,
            "category": result.get("category", "Other"),
            "department": result.get("department", "General"),
            "urgency": result.get("urgency", "Medium"),
            "response": result.get("response", ""),
            "db_summary": result.get("db_summary", ""),
            "faculty_action": result.get("faculty_action", "")
        }

        supabase.table("tickets").insert(data).execute()

        return result

    except Exception as e:
        # THIS prevents 500 crash
        return {
            "response": "System error occurred while processing ticket.",
            "category": "Error",
            "department": "System",
            "urgency": "Low",
            "db_summary": str(e),
            "faculty_action": "Check backend logs"
        }