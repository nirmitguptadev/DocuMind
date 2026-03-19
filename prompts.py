from langchain_core.prompts import ChatPromptTemplate

def get_rag_prompt() -> ChatPromptTemplate:
    """
    Defines the system and human prompt messages for the RAG generation step.
    Returns a structured ChatPromptTemplate.
    """
    
    # The System Prompt tells the AI how to behave and provides the context.
    # The {context} placeholder will be automatically filled by our retriever later.
    system_prompt = (
        "You are a helpful and precise assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the user's question. "
        "If you don't know the answer or if the answer is not contained in the context, "
        "just say that you don't know. Do not try to make up an answer. "
        "Keep the answer concise and strictly based on the provided text.\n\n"
        "Context:\n{context}"
    )

    # The ChatPromptTemplate structures the conversation for Chat Models (like Llama 3)
    # It separates the system instructions from the actual human question.
    # The {input} placeholder will be filled with the user's actual question.
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    return prompt_template

# --- Testing Block ---

if __name__ == "__main__":
    print("Running RAG prompt template test...\n")
    
    # Initialize the prompt template
    prompt = get_rag_prompt()
    
    # Create some dummy data to simulate what the system will actually pass
    dummy_context = "DocuMind is a containerized RAG application built for ETECH LAB project."
    dummy_question = "What is DocuMind?"
    
    try:
        # We use .invoke() to inject our variables into the placeholders
        formatted_prompt = prompt.invoke({
            "context": dummy_context,
            "input": dummy_question
        })
        
        print("Successfully formatted the prompt! Here is what the LLM will actually see:\n")
        print("--------------------------------------------------")
        # Print the system message
        print(f"[SYSTEM MESSAGE]:\n{formatted_prompt.messages[0].content}\n")
        # Print the human message
        print(f"[HUMAN MESSAGE]:\n{formatted_prompt.messages[1].content}")
        print("--------------------------------------------------")
        
    except Exception as e:
        print(f"An error occurred: {e}")