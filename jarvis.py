import requests
import json
from datetime import datetime
from config import MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT_BASE, MAX_HISTORY_PAIRS
from core.memory import get_memory_summary, auto_update_memory
from core.actions.dispatcher import parse_action, dispatch

conversation_history = []


def build_prompt(user_input: str) -> str:
    current_date = datetime.now().strftime("%d/%m/%Y")
    system_prompt = f"{SYSTEM_PROMPT_BASE}\nData atual: {current_date}"
    memory_summary = get_memory_summary()
    history_text = "\n".join(conversation_history) if conversation_history else "Nenhum histórico ainda."

    return f"""{system_prompt}

--- MEMÓRIA PERMANENTE ---
{memory_summary}

--- HISTÓRICO DA SESSÃO ---
{history_text}

Usuário: {user_input}
JARVIS:"""


def ask_jarvis(user_input: str) -> str:

    prompt = build_prompt(user_input)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if response.status_code != 200:
            return f"Erro: {response.status_code}"

        raw = response.json().get("response", "").strip()

    except requests.RequestException as e:
        return f"Erro de conexão: {e}"

    return handle_response(raw)


def handle_response(raw: str) -> str:

    actions_found = []
    search_from = 0

    while True:
        start = raw.find("{", search_from)
        if start == -1:
            break
        end = raw.find("}", start) + 1
        if end == 0:
            break

        depth = 0
        real_end = start
        for i, ch in enumerate(raw[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    real_end = i + 1
                    break

        try:
            candidate = json.loads(raw[start:real_end])
            if "action" in candidate:
                actions_found.append(candidate)
        except json.JSONDecodeError:
            pass

        search_from = real_end

    if not actions_found:
        print(f"JARVIS: {raw}\n")
        return raw

    results = []
    for action_data in actions_found:
        message = action_data.get("message", "Executando...")
        result = dispatch(action_data)
        print(f"JARVIS: {message}")
        print(f"[RESULTADO] {result}\n")
        results.append(f"{message} — {result}")

    return " | ".join(results)


def update_history(user_input: str, response: str):
    conversation_history.append(f"Usuário: {user_input}")
    conversation_history.append(f"JARVIS: {response}")

    max_lines = MAX_HISTORY_PAIRS * 2
    while len(conversation_history) > max_lines:
        conversation_history.pop(0)
        conversation_history.pop(0)


def main():
    print("JARVIS iniciado. Digite 'sair' para encerrar.\n")

    turn_count = 0

    while True:
        try:
            user_input = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando JARVIS.")
            break

        if not user_input:
            continue

        if user_input.lower() == "sair":
            print("Encerrando JARVIS.")
            break

        final_response = ask_jarvis(user_input)
        update_history(user_input, final_response)

        turn_count += 1

        if turn_count % 5 == 0:
            auto_update_memory(conversation_history)


if __name__ == "__main__":
    main()