import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd
import json

# Generate text embeddings
def embed_fn(title, content):
    # Create a new instance of the model
    model = "models/embedding-001"
    embeddings = genai.embed_content(model=model,
                                    title=title,
                                    content=content,
                                    task_type="RETRIEVAL_DOCUMENT")["embedding"] # return just the list of embeddings
    return embeddings

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

json_file = "data/how_teach.json"
language = "pt"

with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

for section in data:
    print(section['title'])
    print(section['content'])
    embeddings = embed_fn(section['title'], section['content'])
    #print(embeddings)
    print("--------------------------------------------------")
    section['embeddings'] = embeddings
    print(section['embeddings'])

new_file = "data/how_teach_embeddings.json"

with open(new_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
