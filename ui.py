import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

def ask_backend(question):
    response = requests.post(API_URL, json={"query": question})
    return response.json()
    
st.set_page_config(page_title="DocuMind", layout="wide")

st.title("DocuMind AI")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("enter the question:")

if st.button("ask"):
    if query:
        result = ask_backend(query)
        answer = result.get("answer", "no response")

        st.session_state.history.append({
            "question": query,
            "answer": answer
        })

for chat in st.session_state.history:
    st.write(f"**you:** {chat['question']}")
    st.write(f"**bot:** {chat['answer']}")
