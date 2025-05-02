from src.embeddings import process_and_embed
from src.retrieval import find_text_relevant
from src.generation import generate_response
import google.generativeai as genai
from dotenv import load_dotenv
import os
import textwrap

# Functions
def to_markdown(text):
  formatted_text = text.replace('*', '')
  return textwrap.indent(formatted_text, ' ', predicate=lambda _: True)

def create_model(model_name):
  # Load the API key from the .env file
  load_dotenv(override=True)
  GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
  genai.configure(api_key=GOOGLE_API_KEY)

  # Create a new instance of the model
  model = genai.GenerativeModel(model_name=model_name)
  return model

def create_chat(model):
  # Start a new chat
  chat = model.start_chat(history=[])
  return chat

def main():
  model_gen = "gemini-1.5-pro"
  model_emb = "models/embedding-001"
  input_json_file = "data/how_teach.json"
  output_json_file = "data/how_teach_embeddings.json"
  
  katron = create_model(model_gen)
  chat = create_chat(katron)

  if not os.path.exists(output_json_file):
    print("Embeddings não encontrados. Gerando...")
    process_and_embed(input_json_file, output_json_file, model_emb)
  else:
    print("Embeddings já existem. Pulando geração.\n")

  print("\nOlá! Eu sou o Katron, seu assistente de estudos de idiomas. Vamos começar?\n")
  print("Digite 'exit' para sair.\n")
  print(to_markdown("Katron: O que vamos estudar hoje?"))
  prompt = input(" User: ")

  prompt_initial = "Eu quero ter uma aula de: "
  first = True

  while prompt != "exit":
      #print(to_markdown(f'user: {prompt}') + '\n')
      if first:
        response = chat.send_message(prompt_initial + prompt)
        first = False
      else:
        texts_relevant = find_text_relevant(prompt, output_json_file, model_emb)
        response = generate_response(prompt, texts_relevant, chat)

      print(to_markdown(f'\nKatron: {response.candidates[0].content.parts[0].text}'))
      print("-------------------------------------------\n")
      prompt = input(" User: ")


if __name__ == "__main__":
    main()