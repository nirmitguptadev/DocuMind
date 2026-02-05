import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def configure_llm():
    """
    Loads the Groq API key and configures the ChatGroq LLM.
    """
    load_dotenv()
    
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Groq API Key not found in environment variables.")
    
    
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.1-8b-instant",
        api_key=groq_api_key
    )
    print("Successfully configured Groq LLM (Llama3-8b).")
    return llm

# --- Testing Block ---
if __name__ == '__main__':
    print("Running Groq LLM configuration test...")
    try:
        chat_llm = configure_llm()
        
        print("\nSending a test message to the Groq API...")
        response = chat_llm.invoke("Tell me 5 points about Manipal University Jaipur")
        
        print("\nSuccessfully received response from Groq:")
        print("--------------------")
        print(response.content)
        print("--------------------")
        
    except Exception as e:
        print(f"\nAn error occurred during the test: {e}")