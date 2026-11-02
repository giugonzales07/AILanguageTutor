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

    assert response == "Resposta simulada"
    assert query in chat.message
    assert "Walk means caminhar." in chat.message
    assert "sem inventar informações" in chat.message