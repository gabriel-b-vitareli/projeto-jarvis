import json
from core.actions import handlers

# Mapa de ações disponíveis
ACTION_MAP = {
    "abrir_url":     handlers.abrir_url,
    "criar_pasta":   handlers.criar_pasta,
    "criar_arquivo": handlers.criar_arquivo,
    "abrir_pasta":   handlers.abrir_pasta,
    "listar_pasta":  handlers.listar_pasta,
}


def parse_action(raw_response: str) -> dict | None:
    """
    Tenta extrair um bloco JSON de ação da resposta do modelo.
    Retorna o dict se encontrar, None caso contrário.
    """
    start = raw_response.find("{")
    end = raw_response.rfind("}") + 1
    if start == -1 or end == 0:
        return None

    try:
        data = json.loads(raw_response[start:end])
        if "action" in data:
            return data
    except json.JSONDecodeError:
        pass

    return None


def dispatch(action_data: dict) -> str:
    """
    Recebe o dict de ação e executa o handler correspondente.
    Retorna o resultado como string para ser exibido/lido pelo TTS.
    """
    action = action_data.get("action")
    params = action_data.get("params", {})

    if action not in ACTION_MAP:
        return f"Ação desconhecida: '{action}'"

    handler = ACTION_MAP[action]

    try:
        return handler(**params)
    except TypeError as e:
        return f"Parâmetros inválidos para '{action}': {e}"