from google import genai 
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIM = 768  # mesmo valor para documentos e perguntas

def get_client() -> genai.Client:
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))