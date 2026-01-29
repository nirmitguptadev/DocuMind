

from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_single_pdf 
from typing import List, Any
import os

def split_documents(documents: List[Any]) -> List[Any]:
    """
    Splits a list of Document objects into smaller chunks.

    Args:
        documents (List[Any]): The list of Document objects to be split.

    Returns:
        List[Any]: A list of smaller Document objects (chunks).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True, # identify the chunk's position
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Successfully split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

# --- Testing Block ---

if __name__ == '__main__':
    print("Running text splitter test...")
    
    
    sample_pdf_path = os.path.join("data", "somatosensory.pdf")
    
    
    if not os.path.exists(sample_pdf_path):
         print(f"Test Error: The sample file was not found at '{sample_pdf_path}'")
    else:
        loaded_documents = load_single_pdf(sample_pdf_path)
    
        
        chunks = split_documents(loaded_documents)
        
        print(f"\nExample of a chunk (the first one):")
        
        
        first_chunk = chunks[0]
        
        print("\n--- Chunk Metadata ---")
        print(first_chunk.metadata)
        
        print("\n--- Chunk Content (first 200 characters) ---")
        print(first_chunk.page_content[:200])
        print("...")
        
        print(f"\nLength of the first chunk: {len(first_chunk.page_content)} characters.")