# config.py

# NEW, correct import from the dedicated package
from langchain_huggingface import HuggingFaceEmbeddings

def configure_embeddings() -> HuggingFaceEmbeddings:
    """
    Configures and returns a local, open-source embeddings model.
    """
    model_name = "all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    print(f"Successfully configured local Hugging Face embeddings model: {model_name}")
    return embeddings

# --- Testing Block ---
if __name__ == '__main__':
    print("Running local embeddings configuration test...")
    try:
        local_embeddings = configure_embeddings()
        
        sample_text = "This is a test to see if the local embedding model is working."
        
        print(f"\nEmbedding the sample text: '{sample_text}'")
        vector = local_embeddings.embed_query(sample_text)
        
        print("\nSuccessfully embedded the text locally!")
        print(f"The resulting vector has {len(vector)} dimensions.")
        print(f"First 5 dimensions of the vector: {vector[:5]}")
        
    except Exception as e:
        print(f"\nAn error occurred during the test: {e}")