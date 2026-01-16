

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def check_gemini_connection():
    """
    Loads the API key from the .env file and then checks the connection 
    to the Google Gemini API by sending a simple prompt.
    """
    
    load_dotenv()
    
    try:
        # Check if the API key is available after loading
        if "GOOGLE_API_KEY" not in os.environ:
            print("Error: GOOGLE_API_KEY not found.")
            print("Please make sure it's set in your .env file.")
            return

        print("API Key loaded. Attempting to connect to the Gemini API...")
        
        # Initialize the ChatGoogleGenerativeAI model
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
        
        # Send a simple message to the model
        response = llm.invoke("Hello, World!")
        
        # Print the response content
        print("\nSuccessfully connected to Gemini!")
        print("Response from Gemini:")
        print("--------------------")
        print(response.content)
        print("--------------------")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your API key in the .env file and your network connection.")

if __name__ == "__main__":
    check_gemini_connection()