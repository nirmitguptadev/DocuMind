from fastapi import FastAPI

# Initialize the FastAPI application
app = FastAPI(
    title="DocuMind API",
    description="Backend API for the DocuMind RAG Application",
    version="1.0.0"
)

@app.get("/")
async def root():
    """
    Root endpoint that welcomes the user.
    """
    return {"message": "Welcome to the DocuMind API. Go to /docs for the API interface."}

@app.get("/health")
async def health_check():
    """
    A simple health check endpoint to verify the server is running.
    This is crucial for Docker and DevOps deployment later.
    """
    return {
        "status": "healthy", 
        "message": "DocuMind API is up and running!"
    }

