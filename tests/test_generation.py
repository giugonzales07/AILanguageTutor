from src.generation import generate_response

class FakeChat:
    def send_message(self, message):
        self.message = message
        return "Resposta simulada"

def test_generate_response_uses_context():
    chat = FakeChat()

    query = "Como falar caminhar em inglês?"
    context = ["Walk means caminhar."]

    response = generate_response(query, context, chat)

    assert response == "Resposta simulada"          # devolveu a resposta do chat
    assert query in chat.message                    # a pergunta do aluno foi enviada
    assert "Walk means caminhar." in chat.message   # o contexto foi enviado
    assert "[Lição de referência]" in chat.message  # a marcação de contexto foi enviada
    assert "[Mensagem do aluno]" in chat.message    # a marcação de pergunta do aluno foi enviada