from src.agent import prepare, create_chat
import logging
import uuid

def main():
  # Show logs only for our code, not for httpx or other libraries
  logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
  logging.getLogger("httpx").setLevel(logging.WARNING)
  logging.getLogger("httpx2").setLevel(logging.WARNING)
  logging.getLogger("google_genai.chats").setLevel(logging.WARNING)

  # create the embeddings and database
  prepare()

  # create a unique session id for this conversation
  session_id = str(uuid.uuid4())

  # create the chat client with the tools
  chat = create_chat(session_id)

  print("\nOlá! Eu sou o Katron, seu assistente de estudos de idiomas. Vamos começar?\n")
  print("(Se quiser encerrar a conversa, basta digitar 'exit')\n")

  print("Katron: Qual seu nome?")
  name = input("User: ")

  print("Katron: O que vamos estudar hoje?")
  prompt = input(f"{name}: ")

  prompt_initial = f"Meu nome é {name} e eu quero ter uma aula de: "
  first = True

  while prompt != "exit":
      message = prompt_initial + prompt if first else prompt
      first = False
      response = chat.send_message(message)  

      print(f'\nKatron: {response.text}')
      print("-----------------------------------------------------------------------------------\n")
      prompt = input(f"{name}: ")


if __name__ == "__main__":
    main()

# Para rodar:
# pipenv shell
# pipenv run python -m src.main