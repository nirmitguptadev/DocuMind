import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"
UPLOAD_URL = "http://localhost:8000/upload"
DOCS_URL = "http://localhost:8000/documents"
CLEAR_URL = "http://localhost:8000/clear"
def ask_backend(question):
    response = requests.post(API_URL, json={"query": question})
    response.raise_for_status()
    return response.json()

def upload_to_backend(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    response = requests.post(UPLOAD_URL, files=files)
    response.raise_for_status()
    return response.json()

def fetch_documents():
    try:
        response = requests.get(DOCS_URL)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"documents": []}

def clear_database():
    response = requests.post(CLEAR_URL)
    response.raise_for_status()
    return response.json()

def display_sources(sources):
    """
    Format and display source documents in an expander.
    """
    if not sources:
        return
    
    with st.expander("View Source Documents"):
        for i, source in enumerate(sources, 1):
            st.markdown(f"**Source {i}**")
            # For pydantic model DocumentSource passed as dict
            metadata = source.get("metadata", {})
            if metadata:
                source_file = metadata.get("source", "Unknown file")
                page = metadata.get("page", "Unknown page")
                st.markdown(f"*File: {source_file} (Page {page})*")
            
            # Display shortened content inside an info box
            content = source.get("page_content", "No content available")
            st.info(content)
            
st.set_page_config(page_title="DocuMind AI", layout="centered", page_icon="🧠")

st.title("🧠 DocuMind AI")
st.markdown("Ask questions about your uploaded documents! The knowledge base uses local embeddings and the Groq LLM.")

# File Uploader Sidebar
with st.sidebar:
    st.header("📄 Upload Document")
    st.markdown("Upload a PDF to expand your knowledge base.")
    
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Upload and Embed"):
            with st.spinner(f"Ingesting '{uploaded_file.name}' into vector DB..."):
                try:
                    result = upload_to_backend(uploaded_file)
                    st.success(result.get("message", "File processed effectively!"))
                except requests.exceptions.RequestException as e:
                    st.error(f"Error communicating with backend: {e}")

    st.divider()
    st.header("🗄️ Database Management")
    
    docs_result = fetch_documents()
    docs = docs_result.get("documents", [])
    
    if docs:
        st.markdown(f"**Embedded files ({len(docs)}):**")
        for doc in docs:
            st.markdown(f"- `{doc}`")
    else:
        st.markdown("*Database is empty.*")
        
    st.divider()
    
    if st.button("Clear Database", type="primary", help="⚠️ WARNING: This will permanently wipe all embedded documents from the database. You will have to re-upload them to chat again."):
        with st.spinner("Wiping DB and refreshing RAG pipeline..."):
            try:
                res = clear_database()
                # Ensure the user's active session history disappears alongside DB logic
                st.session_state.messages = []
                st.success(res.get("message", "Database successfully expunged!"))
                st.rerun()
            except Exception as e:
                st.error(f"Failed to clear database: {e}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            display_sources(message["sources"])

# React to user input
if query := st.chat_input("Ask a question to your document knowledge base..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Searching documents & generating answer..."):
            try:
                result = ask_backend(query)
                answer = result.get("answer", "I could not generate an answer.")
                sources = result.get("sources", [])
                
                # Render answer and sources
                st.markdown(answer)
                if sources:
                    display_sources(sources)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "sources": sources
                })
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with backend API: {e}")
