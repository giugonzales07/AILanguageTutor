import google.generativeai as genai
from dotenv import load_dotenv
import os

# Output
import textwrap

# Functions
def to_markdown(text):
  formatted_text = text.replace('*', '')
  return textwrap.indent(formatted_text, ' ', predicate=lambda _: True)

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Create a new instance of the model
model_name = "gemini-1.5-pro-002"
katron = genai.GenerativeModel(model_name=model_name)

# Start a new chat
chat = katron.start_chat(history=[])

print("\nOlá! Eu sou o Katron, um assistente de estudos. Vamos começar?\n")
print("Digite 'exit' para sair.\n")
print(to_markdown("Katron: O que vamos estudar hoje?"))
prompt = input(" User: ")

prompt_initial = "Eu quero ter uma aula de: "

while prompt != "exit":
    #print(to_markdown(f'user: {prompt}') + '\n')

    response = chat.send_message(prompt_initial + prompt)
    
    print(to_markdown(f'\nKatron: {response.candidates[0].content.parts[0].text}'))
    print("-------------------------------------------\n")
    prompt = input(" User: ")