import prompt

import requests

# Issactoto/therapist-1, TinyLlama/TinyLlama-1.1B-Chat-v1.0
headers = {"Authorization": "Bearer <your_hugging_face_key>"}

def getURL(mode='ft'):
    if(mode=='ft'):
        return "https://api-inference.huggingface.co/models/Issactoto/therapist-3"
    else:
        return "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
def predict(query_string, mode='ft'):
    payload = {
        "inputs": prompt.returnPrompt(query_string, mode),
        "parameters": {
            "max_new_tokens": 250,
            "do_sample": True,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95,
        },
    }
    response = requests.post(getURL(mode), headers=headers, json=payload)
    return response.json()


# queryString = "I am having depression"
# print("output, ", predict(queryString))
