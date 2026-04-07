import os
import subprocess
import webbrowser
from pathlib import Path


def abrir_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Abrindo {url} no navegador."


def criar_pasta(caminho: str) -> str:
    path = Path(caminho).expanduser()
    if path.exists():
        return f"A pasta '{path}' já existe."
    path.mkdir(parents=True, exist_ok=True)
    return f"Pasta criada: {path}"


def criar_arquivo(caminho: str, conteudo: str = "") -> str:
    path = Path(caminho).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return f"O arquivo '{path}' já existe."
    path.write_text(conteudo, encoding="utf-8")
    return f"Arquivo criado: {path}"


def abrir_pasta(caminho: str) -> str:
    path = Path(caminho).expanduser()
    if not path.exists():
        return f"Caminho não encontrado: {path}"
    if os.name == "nt":
        os.startfile(str(path))
    elif os.uname().sysname == "Darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])
    return f"Abrindo pasta: {path}"


def listar_pasta(caminho: str) -> str:
    path = Path(caminho).expanduser()
    if not path.exists():
        return f"Caminho não encontrado: {path}"
    if not path.is_dir():
        return f"'{path}' não é uma pasta."

    itens = list(path.iterdir())
    if not itens:
        return f"A pasta '{path}' está vazia."

    linhas = [f"Conteúdo de '{path}':"]
    for item in sorted(itens):
        tipo = "📁" if item.is_dir() else "📄"
        linhas.append(f"  {tipo} {item.name}")

    return "\n".join(linhas)