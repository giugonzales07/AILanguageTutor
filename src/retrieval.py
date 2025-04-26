# Gerar consulta e buscar nos documentos

from src.ingestion import load_json
import google.generativeai as genai
from dotenv import load_dotenv
import os
import numpy as np

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def embed_query(query, model):
    # Generate the embedding for the query
    response = genai.embed_content(model=model,
                                  content=query,
                                  task_type="RETRIEVAL_QUERY")

    return response['embedding']

def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def find_query(query_embedding, data, top_k=1):    
    # Normalize the query embedding
    query_embedding = normalize(query_embedding)

    dot_product = []
    for section in data:
        # distance between the query and the document
        doc_embedding = normalize(section['embeddings'])
        dot_product.append(np.dot(doc_embedding, query_embedding))
    
    #print(dot_product)

    # get the index of the dot procuct that represents the closest one
    #index = np.argmax(dot_product)
    top_k_indices = np.argsort(dot_product)[-top_k:][::-1]

    results_text = []
    for index in top_k_indices:
        # get the content according to the index
        results_text.append(data[index]["content"])
    return results_text

def find_text_relevant(query, json_file, model):
    query_embedding = embed_query(query, model)
    data = load_json(json_file)

    text_relevant = find_query(query_embedding, data, top_k=1)

    return text_relevant