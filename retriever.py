import os
from langchain_chroma import Chroma
from config import configure_embeddings

# Define where the vector database is saved locally (same as in ingest.py)
DB_PATH = "chroma_db"

def get_retriever():
    """
    Loads the existing Chroma vector database and returns a configured retriever.
    """
    # Check if the database folder exists
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Vector database not found at '{DB_PATH}'. "
            "Please run ingest.py first to create the database."
        )

    # We need the same embedding model to embed the user's search query
    print("Loading local embeddings model for search...")
    embeddings = configure_embeddings()

    # Load the existing database from disk
    print(f"Connecting to vector database at '{DB_PATH}'...")
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    # Create the retriever
    # search_kwargs={"k": 4} tells it to return the top 4 most relevant chunks
    retriever = db.as_retriever(search_kwargs={"k": 4})
    
    print("Retriever successfully configured.")
    return retriever

# --- Testing Block ---

if __name__ == '__main__':
    print("Running retriever test...")
    try:
        # 1. Initialize the retriever
        my_retriever = get_retriever()
        
        # 2. Define a test query
       
        test_query = "What are joint receptors ?"
        print(f"\nSearching for: '{test_query}'")
        
        # 3. Retrieve relevant document chunks using the invoke method
        results = my_retriever.invoke(test_query)
        
        # 4. Display results
        print(f"\nFound {len(results)} relevant chunks.")
        
        if results:
            print("\n--- Top Match (Most Relevant Chunk) ---")
            # Print metadata 
            print(f"Metadata: {results[0].metadata}")
            # Print a preview of the actual text
            print(f"Content preview: {results[0].page_content[:200]}...")
        
    except Exception as e:
        print(f"\nAn error occurred during the test: {e}")