import json
import os
import requests
from config import OLLAMA_URL, MODEL_NAME, MEMORY_EXTRACTION_PROMPT

MEMORY_PATH = "data/long_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_PATH):
        os.makedirs("data", exist_ok=True)
        return {"profile": {}, "projects": [], "preferences": {}, "notes": []}

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory_data):
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)


def add_note(note):
    memory = load_memory()
    if note not in memory["notes"]:
        memory["notes"].append(note)
        save_memory(memory)


def get_memory_summary():
    memory = load_memory()

    profile_text = json.dumps(memory["profile"], ensure_ascii=False) if memory["profile"] else "Nenhum dado ainda."
    projects_text = json.dumps(memory["projects"], ensure_ascii=False) if memory["projects"] else "Nenhum projeto registrado."
    preferences_text = json.dumps(memory["preferences"], ensure_ascii=False) if memory["preferences"] else "Nenhuma preferência registrada."
    notes_text = json.dumps(memory["notes"][-5:], ensure_ascii=False) if memory["notes"] else "Nenhuma nota."

    return f"""Perfil: {profile_text}
Projetos: {projects_text}
Preferências: {preferences_text}
Notas recentes: {notes_text}"""


def _merge_memory(current, extracted):

    if isinstance(extracted.get("profile"), dict):
        current["profile"].update(extracted["profile"])

    if isinstance(extracted.get("projects"), list):
        existing_names = {p.get("name") if isinstance(p, dict) else p for p in current["projects"]}
        for project in extracted["projects"]:
            name = project.get("name") if isinstance(project, dict) else project
            if name not in existing_names:
                current["projects"].append(project)

    if isinstance(extracted.get("preferences"), dict):
        current["preferences"].update(extracted["preferences"])

    if isinstance(extracted.get("notes"), list):
        for note in extracted["notes"]:
            if note and note not in current["notes"]:
                current["notes"].append(note)

    return current


def auto_update_memory(conversation_history: list):

    if not conversation_history:
        return

    current_memory = load_memory()
    conversation_text = "\n".join(conversation_history)

    prompt = MEMORY_EXTRACTION_PROMPT.format(
        current_memory=json.dumps(current_memory, ensure_ascii=False, indent=2),
        conversation=conversation_text
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=30
        )

        if response.status_code != 200:
            return

        raw = response.json().get("response", "").strip()

        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            return

        extracted = json.loads(raw[start:end])
        merged = _merge_memory(current_memory, extracted)
        save_memory(merged)

    except (json.JSONDecodeError, requests.RequestException):
        pass 