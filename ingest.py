import os
from document_loader import load_single_pdf
from text_splitter import split_documents
from config import configure_embeddings
from langchain_chroma import Chroma


DATA_FOLDER = "data"

import chromadb

def ingest_single_pdf_file(file_path: str):
    """
    Ingests a single PDF file: loads, splits, and embeds it into ChromaDB.
    """
    print(f"Loading {file_path} for single ingestion...")
    raw_docs = load_single_pdf(file_path)
    if not raw_docs:
        raise ValueError(f"No documents were loaded from {file_path}")
        
    chunks = split_documents(raw_docs)
    if not chunks:
        raise ValueError("No chunks generated from the document")
    
    print(f" -> Processed {os.path.basename(file_path)}: {len(chunks)} chunks generated.")
    
    print("Initializing Embeddings Model...")
    embeddings = configure_embeddings()
    
    print("Connecting to local ChromaDB at './chroma_db'...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=chroma_client,
        collection_name="documind"
    )
    print("--- Single File Ingestion Complete! ---")
    return len(chunks)

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

    
    print(f"\nConnecting to local ChromaDB at './chroma_db'...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    vector_db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        client=chroma_client,
        collection_name="documind"
    )
    
    print("--- Ingestion Complete! ---")
    print(f"Successfully stored {len(all_chunks)} chunks in the vector database.")

if __name__ == "__main__":
    ingest_documents()