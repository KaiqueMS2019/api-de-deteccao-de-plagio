# API de Detecção de Plágio 

Este projeto é uma API em Python para detecção de plágio com NLP.  
Ele compara textos enviados contra uma **base local** e contra **conteúdos do Wikipedia** usando **embeddings semânticos**.

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

1. **Verificar Plágio** (`/verificar-plagio/`)
   - Recebe arquivo (TXT, DOCX, PDF)
   - Compara com base local e Wikipedia
   - Retorna percentual de similaridade e trechos suspeitos

2. **Adicionar à Base Local** (`/adicionar-base/`)
   - Permite adicionar arquivos novos à base de comparação
   - Atualiza o arquivo `data/base.json` automaticamente

3. **Base Persistente**
   - Textos locais salvos em `data/base.json`
   - API pode ser enriquecida continuamente sem reiniciar

---

## **Instalação e Execução**

### **1. Clonar o repositório**
```bash
git clone <https://github.com/KaiqueMS2019/api-de-deteccao-de-plagio.git>
cd plagio-api
