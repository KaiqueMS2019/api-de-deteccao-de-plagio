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

---

## **2. Criar ambiente virtual e instalar dependências**
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install --upgrade pip
pip install -r requirements.txt

## **3. Rodar a API localmente**
```bash
uvicorn app.main:app --reload
