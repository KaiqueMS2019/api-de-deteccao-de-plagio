import json
import docx
import PyPDF2
import re


def load_base(path="data/base.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []


def read_file(file):
    if file.filename.endswith(".txt"):

        return file.file.read().decode("utf-8")

    elif file.filename.endswith(".docx"):

        doc = docx.Document(file.file)
        return " ".join([p.text for p in doc.paragraphs])

    elif file.filename.endswith(".pdf"):

        reader = PyPDF2.PdfReader(file.file)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() or ""
        return texto

    else:
        raise ValueError(
            "Formato de arquivo não suportado. Use TXT, DOCX ou PDF.")


def normalizar_texto(texto):
    """
    Normaliza texto para comparação semântica:
    - Converte para minúsculas
    - Remove pontuação
    - Remove espaços extras
    """
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()
