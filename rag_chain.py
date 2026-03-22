from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


from retriever import get_retriever
from llm_config import configure_llm
from prompts import get_rag_prompt

def format_docs(docs):
    """
    Helper function to take the list of retrieved Document objects 
    and combine their text into a single string for the prompt.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """
    Assembles the Retrieval-Augmented Generation (RAG) chain using LCEL.
    """
    print("Initializing RAG components...")
    retriever = get_retriever()
    llm = configure_llm()
    prompt = get_rag_prompt()
    
   
    output_parser = StrOutputParser()

    print("Assembling the LCEL chain...")
    
    # --- The LCEL Magic ---
    # 1. The dictionary sets up the inputs for the prompt.
    #    - "context": Takes the user's question, passes it to the retriever, 
    #                 then formats the resulting documents into a string.
    #    - "input": Takes the user's question and passes it straight through unchanged.
    # 2. The data flows into the prompt template to be formatted.
    # 3. The formatted prompt flows into the Groq LLM.
    # 4. The LLM's output flows into the string parser to clean it up.
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )
    
    return rag_chain

# --- Testing Block ---
if __name__ == "__main__":
    print("\n--- Starting RAG Chain Test ---")
    try:
       
        chain = create_rag_chain()
        
        # 2. Define a test question
        
        question = "What are joint receptors?"
        print(f"\nUser Question: '{question}'")
        print("Thinking...\n")
        
        # 3. Invoke the chain! 
       
        answer = chain.invoke(question)
        
        # 4. Print the final answer
        print("--- Final Answer ---")
        print(answer)
        print("--------------------")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")