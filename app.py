import logging
import gradio as gr
import os
from src.agent import prepare, create_chat

# Logs: só os do nosso código
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpx2").setLevel(logging.WARNING)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Limits 
MAX_CHARS = 500
MAX_MESSAGES = 30

prepare()
chats = {}   # session_hash → chat
counts = {}  # session_id → count menssage

def respond(message, history, request: gr.Request):
    session_id = request.session_hash

    if len(message) > MAX_CHARS:
        return f"Sua mensagem tem mais de {MAX_CHARS} caracteres. Por favor, tente algo mais curto."

    counts[session_id] = counts.get(session_id, 0)+1

    if counts[session_id] > MAX_MESSAGES:
        return "Limite de mensagens desta demo atingido. Recarregue a página para começar uma nova sessão."

    if session_id not in chats:
        chats[session_id] = create_chat(session_id)

    try:
        return chats[session_id].send_message(message).text
    except Exception:
        logger.exception("Erro ao chamar o Gemini")
        return "Tive um problema para responder agora. Tente de novo em alguns segundos."
    

demo = gr.ChatInterface(
    fn=respond, 
    title="Katron: tutor de idiomas com IA",
    description=(
        "Um agente que explica gramática com base em lições, registra seus erros "
        "e acompanha seu progresso. Dica: erre de propósito e depois pergunte "
        "quais erros você mais comete."
    ),
    examples=[
        "O que é present perfect?",
        "Yesterday I goed to school",
        "Quais erros eu mais cometo?",
    ],)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))