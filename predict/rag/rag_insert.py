import pinecone
from transformers import AutoTokenizer, AutoModel
import torch

# 
PINECONE_API_KEY='f2d629ac-747d-44d9-84b1-4ccb30d6a067'
PINECONE_ENVIRONMENT='therapist'
file_path = "./data_clean/output/disorders_description.txt" 
index_name = "therapist"
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Step 1: Prepare Your Data (Reading from a Text File)
def read_and_split_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    paragraphs = text.split("<end-of-paragraph>")
    return [p.strip() for p in paragraphs if p.strip()]

data = read_and_split_file(file_path)

# Step 2: Vectorize Your Data
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings[0].numpy()

embeddings = [embed_text(chunk, tokenizer, model) for chunk in data]

# Step 3: Initialize Pinecone Index
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

index = pc.Index(index_name)

# Step 4: Insert Data into Pinecone
items_to_insert = [(str(i), embedding, {"text": data[i]}) for i, embedding in enumerate(embeddings)]
index.upsert(vectors=items_to_insert)
