import prompt

import requests

API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
headers = {"Authorization": "Bearer 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"}


def query(query_string):
    payload = {
        "inputs": prompt.returnPrompt(query_string),
        "parameters": {
            "max_new_tokens": 250,
            "do_sample": True,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95,
        },
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


queryString = "I am suffering from Schizophrenia."
print("output, ", query(queryString))
