import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from typing import Dict, Any, List

# Load the API key from the .env file
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Create a new instance of the model
model_name = "models/embedding-001"

# Embedding training data
#def embed_fn()

# data/how_teach.json

# Função para extrair textos relevantes de uma seção do JSON
def extract_texts_from_section(section: Dict[str, Any], language: str = "pt") -> List[str]:
    """
    Extrai textos relevantes de uma seção do JSON para geração de embeddings.
    Retorna uma lista de textos no idioma especificado.
    """
    texts = []
    
    # Extrair texto do campo "content"
    if "content" in section and language in section["content"]:
        texts.append(section["content"][language])
    
    # Extrair textos do campo "example"
    if "example" in section:
        example = section["example"]
        for key in ["error", "phrase", "correction", "translation", "user_input", "previous_message", "suggested_response", "suggested_feedback"]:
            if key in example and isinstance(example[key], dict) and language in example[key]:
                texts.append(example[key][language])
            elif key in example and isinstance(example[key], str):
                texts.append(example[key])
    
    # Extrair textos do campo "follow_up"
    if "follow_up" in section and "description" in section["follow_up"] and language in section["follow_up"]["description"]:
        texts.append(section["follow_up"]["description"][language])
    if "follow_up" in section and "suggested_follow_up" in section["follow_up"] and language in section["follow_up"]["suggested_follow_up"]:
        texts.append(section["follow_up"]["suggested_follow_up"][language])
    
    # Extrair texto do campo "memory_update" (se existir)
    if "memory_update" in section and language in section["memory_update"]:
        texts.append(section["memory_update"][language])
    
    return texts

# Função para processar o JSON e gerar embeddings
def process_json_and_generate_embeddings(json_file: str, language: str = "pt") -> List[Dict[str, Any]]:
    """
    Processa o JSON, extrai textos e gera embeddings.
    Retorna uma lista de dicionários com textos, embeddings e metadados.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    results = []
    
    for section in data:
        # Extrair metadados da seção
        section_name = section["section"]
        tags = section["tags"]
        
        # Extrair textos relevantes da seção
        texts = extract_texts_from_section(section, language)
        
        # Gerar embeddings para os textos
        #embeddings = generate_embeddings(texts)
        
        # Armazenar resultados com metadados
        for text in texts:
            result = {
                "section": section_name,
                "tags": tags,
                "language": language,
                "text": text,
                #"embedding": embedding
            }
            results.append(result)
    
    return results

json_file = "data/how_teach.json"
language = "pt"

results = process_json_and_generate_embeddings(json_file, language)
new_file = "data/how_teach_embeddings.json"
with open(new_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)
    print("Criado com sucesso")

print("fim")