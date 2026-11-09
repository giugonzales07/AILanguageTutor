from src.embeddings import process_and_embed
from src.config import get_client, GEMINI_MODEL, SYSTEM_PROMPT, EMBEDDINGS_FILE, LESSONS_FILE, DB_FILE
from src.db import init_db
from src.tools import create_tools
from google.genai import types
import os

def prepare():
    # create the embeddings file if it doesn't exist
    if not os.path.exists(EMBEDDINGS_FILE):
        print("Embeddings não encontrados. Gerando...")
        process_and_embed(LESSONS_FILE, EMBEDDINGS_FILE)
    else:
        print("Embeddings já existem. Pulando geração.\n")

    # create the database
    init_db(DB_FILE)

def create_chat(session_id):
    tools = create_tools(session_id)
    
    # create the chat client
    client = get_client()
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=tools) 
    chat = client.chats.create(model=GEMINI_MODEL, config=config, history=[])

    return chat