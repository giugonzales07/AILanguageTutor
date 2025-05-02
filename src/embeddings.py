# Generates embeddings for the content of data

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import pandas as pd
from src.ingestion import load_json

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Generate text embeddings
def embed_file(title, content, model):
    # Create a new instance of the model
    response = genai.embed_content(model=model,
                                    title=title,
                                    content=content,
                                    task_type="RETRIEVAL_DOCUMENT")
    return response["embedding"] # return just the list of embeddings

def save_json(new_json_file, json_file):
    with open(new_json_file, "w", encoding="utf-8") as file:
        json.dump(json_file, file, ensure_ascii=False, indent=2)

def process_and_embed(input_json_file, output_json_file, model):
    json_file = load_json(input_json_file)

    for section in json_file:
        #print(section['title'])
        #print(section['content'])
        embeddings = embed_file(section['title'], section['content'], model)
        #print(embeddings)
        #print("--------------------------------------------------")
        section['embeddings'] = embeddings
        #print(section['embeddings'])

    save_json(output_json_file, json_file)


