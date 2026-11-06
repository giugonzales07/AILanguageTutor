# Generates embeddings for the content of data

from src.ingestion import load_json
from src.config import get_client, EMBEDDING_MODEL, EMBEDDING_DIM
from google.genai import types
import json

# Generate text embeddings
def embed_file(title, content):

    client = get_client() 

    # Create a new instance of the model
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=EMBEDDING_DIM,
        title=title)

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=content,
        config=config)

    return response.embeddings[0].values # return just the list of embeddings

def save_json(new_json_file, json_file):
    with open(new_json_file, "w", encoding="utf-8") as file:
        json.dump(json_file, file, ensure_ascii=False, indent=2)

def process_and_embed(input_json_file, output_json_file):
    json_file = load_json(input_json_file)

    for section in json_file:
        #print(section['title'])
        #print(section['content'])
        embeddings = embed_file(section['title'], section['content'])
        #print(embeddings)
        #print("--------------------------------------------------")
        section['embeddings'] = embeddings
        #print(section['embeddings'])

    save_json(output_json_file, json_file)


