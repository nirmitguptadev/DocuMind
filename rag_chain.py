from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from retriever import get_retriever
from llm_config import configure_llm
from prompts import get_rag_prompt

def format_docs(docs):
    """Combines document content into a single string for the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """
    Assembles the RAG chain to return BOTH the generated answer and the source documents.
    """
    print("Initializing RAG components...")
    retriever = get_retriever()
    llm = configure_llm()
    prompt = get_rag_prompt()
    output_parser = StrOutputParser()

    print("Assembling the advanced LCEL chain...")
    
    # 1. First, we set up a chain that just handles formatting the prompt and generating the text.
    # It expects a dictionary with {"context":[Document objects], "input": "user question"}
    # The .assign() overrides the "context" key, changing it from a list of objects into a single text string.
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | output_parser
    )

    # 2. Now we build the main chain.
    # RunnableParallel creates the initial dictionary by running the retriever and passing the input through.
    # Then, .assign(answer=...) runs the generation chain above and adds the final string under the key "answer".
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "input": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)
    
    return rag_chain_with_source

# --- Testing Block ---
if __name__ == "__main__":
    print("\n--- Starting Advanced RAG Chain Test ---")
    try:
        chain = create_rag_chain()
        
        # Define a test question
        question = "What are joint receptors?"
        print(f"\nUser Question: '{question}'")
        print("Thinking...\n")
        
        # Invoke the chain
        response = chain.invoke(question)
        
        # The response is now a dictionary containing 'input', 'context', and 'answer'
        print("--- Final Answer ---")
        print(response["answer"])
        print("\n--- Sources Used ---")
        
        # Loop through the source documents and print their metadata
        for i, doc in enumerate(response["context"]):
            print(f"Source {i+1}:")
            print(f"  - File: {doc.metadata.get('source', 'Unknown')}")
            # If your text splitter added a page or start_index, it will show up here
            if 'page' in doc.metadata:
                 print(f"  - Page: {doc.metadata['page']}")
            print(f"  - Preview: {doc.page_content[:100]}...\n")
            
        print("--------------------")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")