# Generate the final response to user 

import os

def generate_response(prompt, texts_relevant, chat):
    context = "\n\n".join(texts_relevant) if isinstance(texts_relevant, list) else texts_relevant

    # prompt_complete = (
    #     f"Você é um professor de inglês. Um aluno escreveu a seguinte pergunta:\n"
    #     f"\"{prompt}\"\n\n"
    #     f"Use o conteúdo abaixo como base para responder:\n"
    #     f"{context}\n\n"
    #     f"Responda de forma clara, objetiva, e sem inventar informações que não estejam no texto acima."
    # )

    prompt_complete = (
    "[Lição de referência]\n"
    f"{context}\n\n"
    "[Mensagem do aluno]\n"
    f"{prompt}"
)

    response = chat.send_message(prompt_complete)

    return response