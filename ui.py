import streamlit as st

st.set_page_config(page_title="DocuMind", layout="wide")

st.title("DocuMind AI")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your question:")

if st.button("Ask"):
    if query:
        st.session_state.history.append({"question": query, "answer": "..."})

# Display chat history
for chat in st.session_state.history:
    st.write(f"**You:** {chat['question']}")
    st.write(f"**Bot:** {chat['answer']}")
