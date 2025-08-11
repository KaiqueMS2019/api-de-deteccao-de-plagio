# API de Detecção de Plágio

Este projeto é uma **API de detecção de plágio com NLP** desenvolvida em **Python**.  
A API compara textos enviados contra uma **base local** e contra **conteúdos extraídos do Wikipedia**, utilizando **busca semântica** e **busca léxica**.

---

## **Tecnologias Utilizadas**

- **FastAPI** – Criação da API
- **LangChain + FAISS** – Indexação vetorial e busca semântica
- **Sentence Transformers** – Geração de embeddings multilíngues
- **Wikipedia API** – Busca e extração de conteúdo de artigos
- **PyPDF2 / python-docx** – Extração de texto de PDFs e DOCX
- **Python Multipart** – Upload de arquivos

---

## **Funcionalidades**

1. **Verificar Plágio** (`/compare/`)
   - Recebe arquivo **(TXT, DOCX, PDF)** ou texto puro
   - Compara com a base local e Wikipedia
   - Retorna percentual de similaridade e trechos suspeitos

2. **Adicionar à Base Local** (`/add-to-base/`)
   - Adiciona arquivos/textos novos à base de comparação
   - Atualiza `data/base.json` automaticamente

3. **Health Check** (`/health`)
   - Verifica se a API está no ar

---

## **Instalação Local**

### **1. Clonar o repositório**
```bash
git clone https://github.com/KaiqueMS2019/api-de-deteccao-de-plagio.git
cd api-de-deteccao-de-palgio
```
---

### **2. Criar ambiente virtual e instalar dependências**
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install --upgrade pip
pip install -r requirements.txt
```
## **3. Rodar a API localmente**
```bash
uvicorn app.main:app --reload
```
## **Rodar com Docker**

### **1. Buildar a imagem**
```bash
docker build -t antiplagio:latest .
```
### **2. Buildar a imagem**
```bash
docker run -p 8000:8000 antiplagio:latest
```
## **Testes Automatizados**

Rodar testes unitários localmente:
```bash
# Windows
$env:PYTHONPATH="."; pytest --maxfail=1 --disable-warnings -q

# Linux/macOS
PYTHONPATH=. pytest --maxfail=1 --disable-warnings -q
```
## **Uso da API**
### **1. Via Swagger**
Acesse:
   http://127.0.0.1:8000/docs
   
Como usar:

   Ao acessar, abrira essa pagina:
<img width="1472" height="726" alt="image" src="https://github.com/user-attachments/assets/18b3d441-1242-491b-a862-2f8fa29934da" />
Na rota /compare/, clique no botão "Try it out" e escolha se irá mandar um texto ou um arquivo como uma redação em PDF e clique em "Execute" como na imagema seguir:
<img width="1779" height="666" alt="image" src="https://github.com/user-attachments/assets/d34bc448-a2fa-43af-bae7-0066be243a69" />

Para adicionar mais arquivos na base de dados, na rota /add-to-base/, clique no botão "Try it out" e escolha um arquivo e clique em "Execute" como na imagema seguir:
<img width="1778" height="512" alt="image" src="https://github.com/user-attachments/assets/b50020cc-8aae-4b6b-b12a-c5c006018182" />




