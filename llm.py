import ollama

def rag(context, query, model="deepseek-r1:7b"):
    print(f"RAG with model: {model}")
    try:
        # Build a more clear and specific system message to guide the response
        system_message = (
            "You are an intelligent assistant who generates human-friendly, clear, and relevant answers."
            " You will respond based on the given context and query. Make sure to give precise, natural-sounding responses."
            " Use the context information provided to enhance the accuracy and relevance of the answer."
            "Respond in 100 words"
        )

       
        # Sending the context and query to the Ollama API for response generation
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": system_message},
                {"role": "user", "content": f"Context: {context}\nQuery: {query}"},
            ]
        )
        return response["message"]["content"]

    except Exception as e:
        return f"Error occurred: {str(e)}"
    
def generic(query, model="deepseek-r1:7b"):
    print(f"Generic with model: {model}")
    try:
        # Build a more clear and specific system message to guide the response
        system_message = (
            "You are an intelligent assistant who generates human-friendly, clear, and relevant answers."
            " You will respond based on the given context and query. Make sure to give precise, natural-sounding responses."
            " Answer the query given"
            "Respond in 100 words"
        )

       
        # Sending the context and query to the Ollama API for response generation
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": system_message},
                {"role": "user", "content": f"Query: {query}"},
            ]
        )
        return response["message"]["content"]

    except Exception as e:
        return f"Error occurred: {str(e)}"