import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from src.generation import generate_response

#print("Iniciando o teste...")

# Load the API key from the .env file
#print("Carregando variáveis do .env...")
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#print(f"GOOGLE_API_KEY: {GOOGLE_API_KEY if GOOGLE_API_KEY else 'Não encontrada'}")

#print("Configurando a API do Google...")
genai.configure(api_key=GOOGLE_API_KEY)
#print("Configuração concluída.")


def test_generate_response():
    # Test the generate_response function
    #print("Iniciando test_generate_response...")
    query = "Não sei falar caminhar em inglês, poderia me ajudar a traduzir?"
    texts_relevant = "Quando o aluno estiver com dificuldade para traduzir uma palavra ou frase, ajude-o a entender o significado fornecendo a tradução e o contexto. Incentive-o a usar a palavra em uma frase."
    
    # Create a new instance of the model
    #print("Criando o modelo...")
    model_name = "gemini-1.5-pro"
    start_model = time.time()
    katron = genai.GenerativeModel(model_name=model_name)
    model_time = time.time() - start_model
    #print(f"Modelo criado em {model_time:.2f} segundos")

    #print("Gerando resposta...")
    start_response = time.time()
    response = generate_response(query, texts_relevant, katron)
    response_time = time.time() - start_response

    print(f"Tempo para criar o modelo: {model_time:.2f} segundos")
    print(f"Tempo para gerar a resposta: {response_time:.2f} segundos")
    print(f"Resposta: {response.candidates[0].content.parts[0].text}")
    
    assert response is not None, "Response should not be None"
    assert len(response.candidates) > 0, "Response should have candidates"
    assert isinstance(response.candidates[0].content.parts[0].text, str), "Response text should be a string"
    assert len(response.candidates[0].content.parts[0].text) > 0, "Response text should not be empty"



