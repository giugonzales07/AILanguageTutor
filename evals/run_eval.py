import json
import time
import uuid
import logging
from pathlib import Path
from google.genai import errors

from src.agent import create_chat, prepare
from src.config import LESSONS_FILE
from src.ingestion import load_json

# Logs: só os do nosso código
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpx2").setLevel(logging.WARNING)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

EVAL_DIR = Path(__file__).parent
CASES_FILE = EVAL_DIR / "cases.json"
RESULTS_FILE = EVAL_DIR / "results.md"

def send_with_retry(chat, message, retries=2):
    for attempt in range(retries + 1):
        try:
            return chat.send_message(message)
        except errors.ClientError as e:
            if e.code != 429 or attempt == retries:
                raise
            print("  Limite por minuto atingido, aguardando 60s...")
            time.sleep(60)

def extract_tool_activity(chat):
    """Lê do histórico do chat quais ferramentas foram chamadas e o que devolveram."""
    calls, results = [], []
    for content in chat.get_history():
        for part in content.parts or []:
            if part.function_call:
                calls.append((part.function_call.name, dict(part.function_call.args or {})))
            if part.function_response:
                results.append((part.function_response.name, str(part.function_response.response)))
    return calls, results


def evaluate_case(case, titles):
    chat = create_chat(f"eval-{uuid.uuid4()}")  # conversa nova para cada caso
    response = send_with_retry(chat, case["message"])
    # print(f"Response: \n{response}")
    # print(f"\nHistory chat: \n{chat.get_history()}")
    calls, results = extract_tool_activity(chat)
    # print(f"Calls: {calls}\nResults: {results}")
    called = [name for name, _ in calls]

    expected = case["expected_tool"]
    tool_ok = (not called) if expected is None else (expected in called)

    detail_ok = None
    if expected == "search_lessons" and tool_ok:
        title = titles[case["expected_lesson"]]
        detail_ok = any(f"Lição: {title}" in text for name, text in results if name == "search_lessons")
    elif expected == "log_error" and tool_ok:
        logged = [args.get("error_type") for name, args in calls if name == "log_error"]
        detail_ok = case["expected_error_type"] in logged

    return {"message": case["message"], "expected": expected or "nenhuma",
            "called": ", ".join(called) or "nenhuma", "tool_ok": tool_ok, "detail_ok": detail_ok,
            "response_text": response.text}


def percent(values):
    values = [v for v in values if v is not None]
    return f"{sum(values)}/{len(values)} ({100 * sum(values) / len(values):.0f}%)" if values else "-"


def main():
    prepare()
    titles = {lesson["id"]: lesson["title"] for lesson in load_json(LESSONS_FILE)}
    rows = []
    for case in load_json(CASES_FILE):
        row = evaluate_case(case, titles)
        rows.append(row)
        print(f"{'✅' if row['tool_ok'] else '❌'} {row['message']} → {row['called']} (esperado: {row['expected']})\n")
        if not row["tool_ok"]:
            print(f"   Resposta: {row['response_text'][:200]}")
        # input("Pressione Enter para continuar...")
        time.sleep(12)  # evita estourar o limite de requisições

    search = [r["detail_ok"] for r in rows if r["expected"] == "search_lessons"]
    errors_details = [r["detail_ok"] for r in rows if r["expected"] == "log_error"]
    lines = [
        "| Métrica | Resultado |", "|---|---|",
        f"| Escolha de ferramenta | {percent([r['tool_ok'] for r in rows])} |",
        f"| Lição correta (busca) | {percent(search)} |",
        f"| Categoria correta (erro) | {percent(errors_details)} |",
        "", "| Mensagem | Esperada | Chamada | Ferramenta | Detalhe |", "|---|---|---|---|---|",
    ]
    for r in rows:
        detail = "-" if r["detail_ok"] is None else ("✅" if r["detail_ok"] else "❌")
        lines.append(f"| {r['message']} | {r['expected']} | {r['called']} | {'✅' if r['tool_ok'] else '❌'} | {detail} |")

    RESULTS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[:5]))
    print(f"\nTabela completa salva em {RESULTS_FILE}")


if __name__ == "__main__":
    main()