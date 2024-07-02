import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Prepare the messages in the desired format
messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot who always responds in the style of a pirate",
    },
    {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},
]

# Use the chat template from the tokenizer (mockup as we can't use actual tokenizer methods here)
# Normally, this is where you'd use the `apply_chat_template` method
prompt = "system: You are a friendly chatbot who always responds in the style of a pirate.\nuser: How many helicopters can a human eat in one sitting?"

# Create the payload for the API call
payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 256,
        "do_sample": True,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.95
    }
}

# Send the request to the API and get the response
output = query(payload)

# Extract and print the generated text
generated_text = output[0]["generated_text"]
print(generated_text)