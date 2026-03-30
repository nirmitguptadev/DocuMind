import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from schemas import QueryRequest, QueryResponse, DocumentSource
from rag_chain import create_rag_chain


app = FastAPI(
    title="DocuMind API",
    description="Backend API for the DocuMind RAG Application",
    version="1.0.0"
)

# Initialize the RAG chain when the server starts.

print("Starting up: Initializing RAG chain...")
try:
    rag_chain = create_rag_chain()
    print("RAG chain initialized successfully!")
except Exception as e:
    print(f"Error initializing RAG chain: {e}")
    rag_chain = None

@app.get("/")
async def root():
    return {"message": "Welcome to the DocuMind API. Go to /docs for the interactive API interface."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "DocuMind API is up and running!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Receives a PDF upload, embeds it into ChromaDB, and cleans up the file.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Save the file temporarily in data directory
    temp_file_path = f"data/{file.filename}"
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    try:
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        print(f"File saved to {temp_file_path}, starting embedding process...")
        
        # Ingest the file using the new helper
        from ingest import ingest_single_pdf_file
        num_chunks = ingest_single_pdf_file(temp_file_path)
        
        # Delete file after successful processing as per user request
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {"message": f"Successfully processed and embedded {num_chunks} chunks from {file.filename}."}
        
    except Exception as e:
        # Cleanup on failure
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        print(f"Error during file ingest: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to ingest file: {str(e)}")


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Receives a user question, processes it through the RAG chain, 
    and returns the generated answer along with the source documents.
    """
    # 1. Safety check
    if not rag_chain:
        raise HTTPException(status_code=500, detail="RAG chain is not initialized. Check server logs.")

    try:
        print(f"Received query: '{request.query}'")
        
        # 2. Pass the user's question from the Pydantic schema into the LCEL chain
        response = rag_chain.invoke(request.query)
        
        # 3. Extract the answer and source documents from the chain's dictionary output
        answer_text = response.get("answer", "I could not generate an answer.")
        source_docs = response.get("context",[])
        
        # 4. Format the source documents to match our Pydantic DocumentSource schema
        formatted_sources =[]
        for doc in source_docs:
            formatted_sources.append(
                DocumentSource(
                    page_content=doc.page_content,
                    metadata=doc.metadata
                )
            )
        
        # 5. Return the final structured response (FastAPI converts this to JSON automatically!)
        return QueryResponse(
            answer=answer_text,
            sources=formatted_sources
        )
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {str(e)}")