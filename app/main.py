from fastapi import FastAPI, UploadFile, File
from app.utils import load_base, read_file
from app.plagiarism import plagiarism_check
import json

app = FastAPI(title="API Detecção de Plágio")

base_local = load_base()


@app.post("/verificar-plagio/")
async def verificar_plagio(file: UploadFile = File(...)):
    try:
        texto = read_file(file)
        percentual, suspeitos = plagiarism_check(texto, base_local)

        return {
            "percentual_plagio": f"{percentual:.2f}%",
            "suspeitos": suspeitos
        }
    except Exception as e:
        return {"erro": str(e)}


@app.post("/adicionar-base/")
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
