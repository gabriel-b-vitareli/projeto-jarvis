import requests
import json
import sys
from datetime import datetime
from config import MODEL_NAME, OLLAMA_URL, SYSTEM_PROMPT_BASE, MAX_HISTORY_PAIRS
from core.memory import get_memory_summary, auto_update_memory

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


def ask_jarvis_stream(user_input: str) -> str:
    """Envia a pergunta ao Ollama com streaming e exibe a resposta em tempo real."""
    prompt = build_prompt(user_input)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    full_response = []

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60) as response:
            if response.status_code != 200:
                return f"Erro: {response.status_code}"

            print("JARVIS: ", end="", flush=True)

            for line in response.iter_lines():
                if not line:
                    continue

                chunk = json.loads(line)
                token = chunk.get("response", "")
                print(token, end="", flush=True)
                full_response.append(token)

                if chunk.get("done"):
                    break

        print("\n")  # Quebra de linha após a resposta completa

    except requests.RequestException as e:
        return f"Erro de conexão: {e}"

    return "".join(full_response).strip()


def update_history(user_input: str, response: str):
    """Adiciona ao histórico e mantém o limite de pares configurado."""
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

        response = ask_jarvis_stream(user_input)
        update_history(user_input, response)

        turn_count += 1

        # Atualiza memória a cada 5 turnos de conversa
        if turn_count % 5 == 0:
            auto_update_memory(conversation_history)


if __name__ == "__main__":
    main()