import streamlit as st

st.set_page_config(page_title="DocuMind", layout="wide")

st.title("📄 DocuMind AI")
st.write("ask your questions about the documents")

query = st.text_input("enter the question:")

if st.button("ask"):
    st.write("the response will appear here...")
