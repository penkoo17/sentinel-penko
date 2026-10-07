@echo off
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -q -r requirements.txt
start "" uvicorn app.main:app --host 0.0.0.0 --port 8000
timeout /t 2 >nul
streamlit run ui/streamlit_app.py