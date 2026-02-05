import os
from document_loader import load_single_pdf
from text_splitter import split_documents
from config import configure_embeddings
from langchain_community.vectorstores import Chroma


DATA_FOLDER = "data"

DB_PATH = "chroma_db"

def ingest_documents():
    """
    Loads PDFs, splits them into chunks, and stores them in a local ChromaDB.
    """
   
    if not os.path.exists(DATA_FOLDER):
        print(f"Error: Data folder '{DATA_FOLDER}' not found.")
        return

    # 2. Load all PDF files in the data directory
    all_chunks = []
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the data directory.")
        return

    print(f"Found {len(pdf_files)} PDF(s) to process.")

    for filename in pdf_files:
        file_path = os.path.join(DATA_FOLDER, filename)
        print(f"Loading {filename}...")
        
        try:
           
            raw_docs = load_single_pdf(file_path)
            
            
            chunks = split_documents(raw_docs)
            all_chunks.extend(chunks)
            print(f" -> Processed {filename}: {len(chunks)} chunks generated.")
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    if not all_chunks:
        print("No document chunks to store.")
        return

    
    print("\nInitializing Embeddings Model...")
    embeddings = configure_embeddings()

    
    print(f"\nCreating Vector Store at '{DB_PATH}'...")
    
    
    vector_db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print("--- Ingestion Complete! ---")
    print(f"Successfully stored {len(all_chunks)} chunks in the vector database.")

if __name__ == "__main__":
    ingest_documents()