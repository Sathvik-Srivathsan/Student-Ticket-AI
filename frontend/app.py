import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import requests
import pandas as pd

from db.supabase_client import supabase


# ----------------------------
# Fetch tickets from DB
# ----------------------------
def fetch_tickets():
    try:
        res = supabase.table("tickets").select("*").order("id", desc=True).execute()
        return res.data or []
    except Exception as e:
        st.error(f"DB error: {e}")
        return []


# ----------------------------
# UI Setup
# ----------------------------
st.set_page_config(page_title="Student Ticket AI", page_icon="🎫")

st.title("🎫 Student Ticket AI System")
st.markdown("Describe your issue in natural language. The system will auto-categorize it.")

mode = st.radio("Mode", ["Student", "Admin"])


# ============================
# STUDENT MODE
# ============================
if mode == "Student":

    user_text = st.text_area("Your Issue", height=150)

    if st.button("Submit Ticket"):

        if not user_text.strip():
            st.warning("Please enter a valid issue.")

        else:
            with st.spinner("Processing ticket..."):

                try:
                    res = requests.post(
                        "http://127.0.0.1:8000/create-ticket",
                        json={"text": user_text},
                        timeout=30
                    )

                    if res.status_code != 200:
                        st.error("Backend error occurred")
                        st.text(res.text)

                    else:
                        data = res.json()

                        st.success("Ticket Submitted Successfully 🎉")

                        st.divider()

                        st.subheader("💬 Response")
                        st.success(data.get("response", "No response"))

                        st.subheader("📌 Details")
                        st.write(f"**Category:** {data.get('category', 'N/A')}")
                        st.write(f"**Department:** {data.get('department', 'N/A')}")
                        st.write(f"**Urgency:** {data.get('urgency', 'N/A')}")

                        st.subheader("🧠 Faculty Action")
                        st.info(data.get("faculty_action", "N/A"))

                        st.subheader("📝 Internal Summary")
                        st.caption(data.get("db_summary", ""))

                except requests.exceptions.ConnectionError:
                    st.error("Backend not running (FastAPI offline)")

                except requests.exceptions.Timeout:
                    st.error("Request timed out (Gemini slow)")

                except Exception as e:
                    st.error(f"Unexpected error: {e}")


# ============================
# ADMIN MODE
# ============================
elif mode == "Admin":

    st.subheader("📜 Ticket History")

    tickets = fetch_tickets()

    if not tickets:
        st.info("No tickets found.")
    else:

        # CSV EXPORT (IMPORTANT FEATURE)
        df = pd.DataFrame(tickets)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Tickets CSV",
            csv,
            "tickets.csv",
            "text/csv"
        )

        st.divider()

        for t in tickets:
            with st.container():
                st.markdown("---")

                st.write(f"**Issue:** {t.get('user_text')}")
                st.write(f"**Category:** {t.get('category')}")
                st.write(f"**Urgency:** {t.get('urgency')}")
                st.write(f"**Department:** {t.get('department')}")
                st.info(f"Action: {t.get('faculty_action')}")