import ollama

response = ollama.chat(
    model='deepseek-r1:7b',
    messages=[
        {
            'role': 'user',
            'content': 'What is the capital of Cambodia?'
        },
    ]
)

print(response['message']['content'])