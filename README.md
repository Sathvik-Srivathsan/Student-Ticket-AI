# Student Ticket AI System

An AI-powered university helpdesk system that automatically classifies student complaints, generates responses, assigns urgency, and stores structured tickets in a database.

frontend/app.py (Streamlit): Takes user issue input, sends it to backend, and displays the processed ticket result in a UI.
backend/main.py (FastAPI): Exposes API endpoints (like /create-ticket) that receive text and return processed ticket data.
backend/llm_service.py: Sends the complaint text to Gemini and converts the response into structured JSON (category, urgency, etc.).
db/supabase_client.py: Creates and exports the Supabase client used to insert/fetch tickets from the database.
run_project.py: Starts backend (FastAPI) and frontend (Streamlit) together so you don’t run two terminals.
.env → Stores secret keys (Gemini + Supabase credentials) used by backend services.

<img width="472" height="750" alt="image" src="https://github.com/user-attachments/assets/40914cc7-a22a-4775-b615-4de8735986c4" />

<img width="483" height="827" alt="image" src="https://github.com/user-attachments/assets/e4d57a6d-c07f-4476-892d-1cbb0251490e" />


# Dependencies

    pip install -r requirements.txt

# Add .env

        GEMINI_API_KEY=your_key
        SUPABASE_URL=your_url
        SUPABASE_KEY=your_key
