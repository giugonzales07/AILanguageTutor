# Generete embeddings for the query and find the most relevant text in the documents

from src.ingestion import load_json
from src.config import get_client, EMBEDDING_MODEL, EMBEDDING_DIM
from google.genai import types
import numpy as np

def embed_query(query):
    # Generate the embedding for the query
    client = get_client()

    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=EMBEDDING_DIM)
    
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=config)

    return response.embeddings[0].values

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

    results = []
    for index in top_k_indices:
        results.append(data[index])

    return results
