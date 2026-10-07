#!/bin/bash
set -e

if [ ! -d "venv" ]; then
    python -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!
trap "kill $API_PID" EXIT

sleep 2
streamlit run ui/streamlit_app.py