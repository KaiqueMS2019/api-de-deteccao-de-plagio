from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from app.utils import load_base, read_file
from app.plagiarism import plagiarism_check
import json

app = FastAPI(title="API Detecção de Plágio")

base_local = load_base()


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}


@app.post("/compare/")
async def verificar_plagio(file: Optional[UploadFile] = File(None),
                           texto_manual: Optional[str] = Form(None)):
    try:
        if file:
            texto = read_file(file)
        elif texto_manual:
            texto = texto_manual
        else:
            return {"erro": "Envie um arquivo ou escreva um texto."}

        resultado = plagiarism_check(texto, base_local, threshold=0.7, top_k=5)

        return resultado

    except Exception as e:
        return {"erro": str(e)}


@app.post("/add-to-base/")
async def adicionar_base(file: UploadFile = File(...)):
    try:
        texto = read_file(file)

        with open("data/base.json", "r", encoding="utf-8") as f:
            base = json.load(f)

        novo_item = {"texto": texto, "fonte": file.filename}
        base.append(novo_item)

        with open("data/base.json", "w", encoding="utf-8") as f:
            json.dump(base, f, ensure_ascii=False, indent=2)

        global base_local
        base_local = load_base()

        return {"mensagem": f"Arquivo '{file.filename}' adicionado à base com sucesso."}

    except Exception as e:
        return {"erro": str(e)}
