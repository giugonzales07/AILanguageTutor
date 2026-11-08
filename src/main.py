from src.embeddings import process_and_embed
from src.config import get_client, GEMINI_MODEL, SYSTEM_PROMPT, EMBEDDINGS_FILE, LESSONS_FILE, DB_FILE
from src.db import init_db
from src.tools import create_tools
from google.genai import types
import os
import logging
import uuid

def main():
  # Show logs only for our code, not for httpx or other libraries
  logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
  logging.getLogger("httpx").setLevel(logging.WARNING)
  logging.getLogger("httpx2").setLevel(logging.WARNING)
  logging.getLogger("google_genai.chats").setLevel(logging.WARNING)

  # create the embeddings file if it doesn't exist
  if not os.path.exists(EMBEDDINGS_FILE):
    print("Embeddings não encontrados. Gerando...")
    process_and_embed(LESSONS_FILE, EMBEDDINGS_FILE)
  else:
    print("Embeddings já existem. Pulando geração.\n")

  # create the database
  init_db(DB_FILE)

  # create a unique session id for this conversation and the tools
  session_id = str(uuid.uuid4())
  tools = create_tools(session_id)

  # create the chat client
  client = get_client()
  config = types.GenerateContentConfig(
     system_instruction=SYSTEM_PROMPT,
     tools=tools) 
  chat = client.chats.create(model=GEMINI_MODEL, config=config, history=[])

  print("\nOlá! Eu sou o Katron, seu assistente de estudos de idiomas. Vamos começar?\n")
  print("(Se quiser encerrar a conversa, basta digitar 'exit')\n")

  print("Katron: Qual seu nome?")
  name = input("User: ")

  print("Katron: O que vamos estudar hoje?")
  prompt = input(f"{name}: ")

  prompt_initial = f"Meu nome é {name} e eu quero ter uma aula de: "
  first = True

  while prompt != "exit":
      message = prompt_initial + prompt if first else prompt
      first = False
      response = chat.send_message(message)  

      print(f'\nKatron: {response.text}')
      print("-----------------------------------------------------------------------------------\n")
      prompt = input(f"{name}: ")


if __name__ == "__main__":
    main()

# Para rodar:
# pipenv shell
# pipenv run python -m src.main