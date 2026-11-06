import logging

from src.config import DB_FILE, EMBEDDINGS_FILE, LESSONS_FILE
from src.db import save_error, top_errors
from src.ingestion import load_json
from src.retrieval import embed_query, find_query

logger = logging.getLogger(__name__)

def create_tools(session_id: str, db_path=DB_FILE):
    valid_types = {lesson["id"] for lesson in load_json(LESSONS_FILE)} | {"other"}

    def search_lessons(topic: str) -> str:
        """Busca na base de lições de inglês a explicação de um tópico gramatical ou de vocabulário.

        Use antes de explicar uma regra gramatical, quando o aluno pedir uma explicação
        ("o que é present perfect?") ou quando você precisar de exemplos confiáveis para
        corrigir um erro. Baseie sua explicação no conteúdo retornado.

        Não use para cumprimentos, agradecimentos, conversa livre ou assuntos fora do
        aprendizado de idiomas.

        Args:
            topic: o tópico em poucas palavras, de preferência em inglês.
                Exemplos: "present perfect", "prepositions of time", "false cognates".

        Returns:
            O título e o conteúdo da lição mais relevante.
        """
        logger.info("search_lessons(topic=%r)", topic)
        query_embedding = embed_query(topic)
        lessons = load_json(EMBEDDINGS_FILE)
        best = find_query(query_embedding, lessons, top_k=1)[0]
        return f"Lição: {best['title']}\n\n{best['content']}"


    def log_error(error_type: str, sentence: str, correction: str) -> str:
        """Registra um erro de inglês cometido pelo aluno, para acompanhar o progresso dele.

        Use sempre que corrigir um erro gramatical ou de vocabulário na frase do aluno,
        um registro por erro corrigido. Não registre erros de digitação nem frases
        que estavam corretas.

        Args:
            error_type: a categoria do erro. Use exatamente um destes valores:
                "verb-to-be", "simple-present", "present-continuous",
                "simple-past-regular", "simple-past-irregular", "present-perfect",
                "present-perfect-vs-simple-past", "will-vs-going-to", "articles",
                "prepositions-time", "prepositions-place", "much-many",
                "comparatives-superlatives", "modals", "false-cognates".
                Se nenhum se aplicar, use "other".
            sentence: a frase original do aluno, com o erro. Exemplo: "Yesterday I goed to school".
            correction: a frase corrigida. Exemplo: "Yesterday I went to school".

        Returns:
            Uma confirmação de que o erro foi registrado.
        """
        logger.info("log_error(error_type=%r)", error_type)
        error_type = error_type.strip().lower()
        if error_type not in valid_types:
            logger.warning("Tipo de erro desconhecido %r; usando 'other'", error_type)
            error_type = "other"
        save_error(db_path, session_id, error_type, sentence, correction)
        return f"Erro registrado: {error_type}."

    def get_progress() -> str:
        """Consulta os erros mais frequentes do aluno nesta sessão.

        Use quando o aluno perguntar sobre o próprio progresso ("quais erros eu mais
        cometo?", "no que preciso melhorar?") ou quando quiser sugerir uma revisão
        com base nos erros dele.

        Returns:
            Os tipos de erro mais frequentes com a quantidade de cada um,
            ou um aviso de que ainda não há erros registrados.
        """
        logger.info("get_progress()")
        rows = top_errors(db_path, session_id)
        if not rows:
            return "Nenhum erro registrado nesta sessão."
        summary = "; ".join(f"{error_type}: {count}" for error_type, count in rows)
        return f"Erros mais frequentes nesta sessão: {summary}."

    return [search_lessons, log_error, get_progress]