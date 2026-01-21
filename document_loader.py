

from langchain_community.document_loaders import PyPDFLoader
from typing import List
import os
from typing import Any 

def load_single_pdf(file_path: str) -> List[Any]:
    """
    Loads a single PDF document from the given file path.

    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file was not found at the specified path: {file_path}")
        
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    print(f"Successfully loaded {len(documents)} pages from {os.path.basename(file_path)}")
    return documents


if __name__ == '__main__':
    print("Running document loader test...")
    
    
    sample_pdf_path = os.path.join("data", "somatosensory.pdf")

    
    if not os.path.exists(sample_pdf_path):
        print(f"Test Error: The sample file was not found at '{sample_pdf_path}'")
        print("Please make sure you have a 'data' folder with a 'sample.pdf' file in it.")
    else:
        
        loaded_documents = load_single_pdf(sample_pdf_path)
        
        
        print(f"Total number of pages loaded: {len(loaded_documents)}")
        
        
        first_page = loaded_documents[0]
        
        
        
        print("\nFirst Page Content")
        print(first_page)
        print("...")