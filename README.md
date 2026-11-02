# AILanguageTutor

An intelligent language tutor built with **Python** and the **Google Gemini API**. It provides an interactive way to learn new languages with the help of an AI-powered assistant.

> **Status:** in active development. The project currently runs in your terminal. A web interface is coming soon, and a new feature using RAG techniques will be added.

![Demo](docs/demo.gif)
<!-- Add a short GIF or screenshot of a real session in docs/demo.gif -->

## How it works

1. **Embeddings:** on the first run, the teaching material in `data/how_teach.json` is converted into embeddings (`models/embedding-001`) and cached in `data/how_teach_embeddings.json`.
2. **Retrieval:** for each user question, the most relevant passages are retrieved [by cosine similarity, top-k = N — confirm].
3. **Generation:** the retrieved passages and the chat history are sent to Gemini (`gemini-2.0-flash-lite`), which answers as **Katron**, the tutor. [Confirm how the context is injected into the prompt.]

The tutor interface is in **Portuguese**.


## Example session

```text
Olá! Eu sou o Katron, seu assistente de estudos de idiomas. Vamos começar?

Se quiser encerrar a conversa, basta digitar 'exit'.

 Katron: Qual seu nome?
 User:Giuliano
 Katron: O que vamos estudar hoje?
 Giuliano: Inglês

 Katron: Hello, Giuliano! It's very nice to meet you. Welcome to your first English class!

 Since this is our very first time talking, let's start with a quick and easy warm-up.

 Can you answer this question in English? (Don't worry about making mistakes!)

 "How are you today, Giuliano?"
 (Como você está hoje?)

 (You can answer something like: "I am fine, thank you", or "I'm a little tired, but excited", or just however you feel!)
-----------------------------------------------------------------------------------

 Giuliano:
```

## Technologies

<p>
  <img alt="Python" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">
  <img alt="Pandas" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg">
</p>

**Python version and environment management**
- **pyenv:** manages multiple Python versions on a single machine.
- **Pipenv:** manages project dependencies and virtual environments.

**LLM**
- **Gemini:** Google's large language model, which powers the natural language understanding and generation behind the tutor.

## Getting started

### Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) and [Pipenv](https://pipenv.pypa.io/)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### Installation

```bash
git clone https://github.com/giugonzales07/AILanguageTutor.git
cd AILanguageTutor
pyenv install            # uses the version in .python-version
pipenv install
```

### Configuration

Copy the example file and add your key:

```bash
cp .env.example .env
```

```text
GOOGLE_API_KEY=your-key-here
```

Never commit your `.env` file.

### Run

```bash
pipenv run python [path/to/entry_point.py]
```

### Tests

```bash
pipenv run [pytest]
```

## Project structure

```text
├── src/          # application code
├── tests/        # automated tests
├── notebooks/    # exploration
├── Pipfile       # dependencies
└── README.md
```

## Roadmap

- [x] Terminal chat with the Gemini API
- [x] Basic RAG over a teaching-material knowledge base
- [ ] Evaluation set to measure answer quality and retrieval
- [ ] Simple web interface
- [ ] Docker image and CI to run the tests

## Author

**Giuliano Gonzales**: [LinkedIn](https://www.linkedin.com/in/giulianogonzales/)
