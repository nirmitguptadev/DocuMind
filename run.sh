#!/bin/bash
# Start FastAPI backend in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for the backend to start
sleep 5

# Start Streamlit frontend in the foreground
streamlit run ui.py --server.port 7860 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false

# If Streamlit exits, kill the backend
kill $BACKEND_PID
