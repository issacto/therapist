import pinecone
from transformers import AutoTokenizer, AutoModel
import torch

PINECONE_API_KEY='<your_pinecone_key>'
PINECONE_ENVIRONMENT='therapist'
file_path = "./data_clean/output/disorders_description.txt" 
index_name = "therapist"


# Step 2: Vectorize Your Data
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Step 3: Initialize Pinecone Index
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

index = pc.Index(index_name)

def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings[0].numpy()


# Step 5: Query the Pinecone Index
def rag_query(query_text):
    query_embedding = embed_text(query_text, tokenizer, model).tolist()
    # print("query_embedding ",query_embedding)
    result = index.query(vector=query_embedding, top_k=1, include_metadata=True)
    # print("result ",result)

    # Print results
    response = None
    for match in result['matches']:
        print('match ',match)
        print(f"ID: {match['id']}, Score: {match['score']}")
        if(match['score']>=0.4):
            response=match['metadata']['text']
    return response
