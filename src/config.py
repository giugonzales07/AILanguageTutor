from google import genai 
from dotenv import load_dotenv
from pathlib import Path
import os
from functools import cache

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIM = 768  # mesmo valor para documentos e perguntas

ROOT = Path(__file__).resolve().parent.parent  # src/config.py → raiz do projeto
SYSTEM_PROMPT = (ROOT / "prompts" / "katron.md").read_text(encoding="utf-8")

LESSONS_FILE = (ROOT / "data" / "lessons.json")
EMBEDDINGS_FILE = (ROOT / "data" / "lessons_embeddings.json")

DB_FILE = (ROOT / "data" / "errors.db")

@cache
def get_client() -> genai.Client:
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))