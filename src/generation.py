# Generate the final response to user 

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_response(prompt, texts_relevant, model):
    prompt_complete = f"Responda o aluno que escreveu: {prompt} para te guiar em como responder siga as instruções a seguir: {texts_relevant}. Lembre que você é um professor de inglês e deve responder o aluno como se fosse um professor. Não adicione informações que não façam parte do texto. Responda de forma clara e objetiva."

    response = model.generate_content(prompt_complete)

    return response