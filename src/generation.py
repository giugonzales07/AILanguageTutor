# Generate the final response to user 

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_response(prompt, texts_relevant, chat):
    context = "\n\n".join(texts_relevant) if isinstance(texts_relevant, list) else texts_relevant

    #prompt_complete = f"Responda o aluno que escreveu: {prompt} para te guiar em como responder siga as instruções a seguir: {context}. Lembre que você é um professor de inglês e deve responder o aluno como se fosse um professor. Não adicione informações que não façam parte do texto. Responda de forma clara e objetiva."

    prompt_complete = (
        f"Você é um professor de inglês. Um aluno escreveu a seguinte pergunta:\n"
        f"\"{prompt}\"\n\n"
        f"Use o conteúdo abaixo como base para responder:\n"
        f"{context}\n\n"
        f"Responda de forma clara, objetiva, e sem inventar informações que não estejam no texto acima."
    )

    response = chat.send_message(prompt_complete)

    return response