from src.embeddings import process_and_embed
from src.retrieval import find_text_relevant
from src.generation import generate_response
from src.config import get_client, GEMINI_MODEL, SYSTEM_PROMPT, EMBEDDINGS_FILE, LESSONS_FILE
from google.genai import types
import os
import textwrap

# Functions
# def to_markdown(text):
#   formatted_text = text.replace('*', '')
#   return textwrap.indent(formatted_text, ' ', predicate=lambda _: True)

def main():
  input_json_file = LESSONS_FILE
  output_json_file = EMBEDDINGS_FILE

  client = get_client()

  config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT) 
  chat = client.chats.create(model=GEMINI_MODEL, config=config, history=[])

  if not os.path.exists(output_json_file):
    print("Embeddings não encontrados. Gerando...")
    process_and_embed(input_json_file, output_json_file)
  else:
    print("Embeddings já existem. Pulando geração.\n")

  print("\nOlá! Eu sou o Katron, seu assistente de estudos de idiomas. Vamos começar?\n")
  print("Se quiser encerrar a conversa, basta digitar 'exit'.\n")
  # print(to_markdown("Katron: Qual seu nome?"))
  print("Katron: Qual seu nome?")
  name = input("User: ")
  # print(to_markdown("Katron: O que vamos estudar hoje?"))
  print("Katron: O que vamos estudar hoje?")
  prompt = input(f"{name}: ")

  prompt_initial = f"Meu nome é {name} e eu quero ter uma aula de: "
  first = True

  while prompt != "exit":
      #print(to_markdown(f'user: {prompt}') + '\n')
      if first:
        response = chat.send_message(prompt_initial + prompt)
        first = False
      else:
        texts_relevant = find_text_relevant(prompt, output_json_file)
        response = generate_response(prompt, texts_relevant, chat)

      # print(to_markdown(f'\nKatron: {response.text}'))
      print(f'\nKatron: {response.text}')
      print("-----------------------------------------------------------------------------------\n")
      prompt = input(f"{name}: ")


if __name__ == "__main__":
    main()

# Para rodar:
# pipenv shell
# pipenv run python -m src.main