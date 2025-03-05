import ollama


def generate_embeddings(text, model='nomic-embed-text'):
    """
    Generate embeddings for a given text using the specified model.
    -----
    :param text: The text to generate embeddings for.
    :param model: The model to use for generating embeddings.
    :return: The embeddings for the given text.
    """
    # Remove newlines and trailing whitespace
    text = text.replace('\n', ' ').strip()

    return ollama.embeddings(
        model=model,
        prompt=text
    ).embedding

if __name__ == '__main__':
    text = "What is the capital of Cambodia?"

    emb = ollama.embeddings(
        model='nomic-embed-text',
        prompt=text
    )

    print(emb)



if __name__ == '__main__':
    text = "What is the capital of Cambodia?"

    emb = generate_embeddings(text)

    print(emb)