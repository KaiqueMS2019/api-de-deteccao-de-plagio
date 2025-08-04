from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from sentence_transformers import util
from app.utils import normalizar_texto
import wikipedia

wikipedia.set_lang("pt")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def chunk_text(texto, chunk_size=300, overlap=50):
    """
    Divide texto em pedaços menores (chunks) para análise mais granular.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(texto)


def create_faiss_index(docs):
    """
    Cria índice FAISS a partir de uma lista de textos.
    """
    return FAISS.from_texts(docs, embedding_model)


def buscar_artigos_wikipedia(termo_busca, max_artigos=3):
    """
    Busca artigos no Wikipedia com duas estratégias:
    1. Palavra-chave principal (removendo stopwords)
    2. Frase curta resumida (2-3 palavras principais)
    Faz fallback PT -> EN se não encontrar nada.
    """
    try:

        stopwords = {
            "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das",
            "em", "para", "por", "e", "que", "com", "no", "na", "nos", "nas",
            "is", "in", "the", "an", "of", "and"
        }

        palavras = [p for p in termo_busca.split() if p.lower()
                    not in stopwords]

        termo_curto = palavras[0] if palavras else termo_busca

        termo_frase_curta = " ".join(palavras[:3]) if len(
            palavras) >= 2 else termo_curto

        termos_busca = [termo_curto, termo_frase_curta]

        artigos_chunks = []

        for termo in termos_busca:
            for lang in ["pt", "en"]:
                wikipedia.set_lang(lang)
                print(
                    f"[Wikipedia] ({lang}) Buscando artigos para termo: '{termo}'")

                titulos = wikipedia.search(termo, results=max_artigos)
                print(f"[Wikipedia] Títulos encontrados ({lang}): {titulos}")

                for titulo in titulos:
                    try:
                        pagina = wikipedia.page(titulo)
                        conteudo = pagina.content
                        print(
                            f"[Wikipedia] Artigo '{titulo}' carregado ({lang}), tamanho: {len(conteudo)} chars")

                        texto_norm = normalizar_texto(conteudo)
                        artigos_chunks.extend(chunk_text(texto_norm))

                    except wikipedia.exceptions.DisambiguationError:
                        continue
                    except Exception as e:
                        print(
                            f"[Wikipedia] Erro ao processar artigo '{titulo}' ({lang}): {e}")
                        continue

        artigos_chunks = list(set(artigos_chunks))

        return artigos_chunks

    except Exception as e:
        print(f"[Wikipedia] Erro geral: {e}")
        return []


def plagiarism_check(user_text, base_local, threshold=0.7):
    """
    1. Normaliza e divide texto do usuário
    2. Cria FAISS com base local
    3. Busca artigos no Wikipedia e adiciona ao FAISS
    4. Compara chunks do usuário contra FAISS
    5. Retorna percentual de plágio e trechos suspeitos
    """
    try:

        user_text = normalizar_texto(user_text)
        chunks_user = chunk_text(user_text)
        if not chunks_user:
            return 0, [{"erro": "Texto muito curto para análise"}]

        textos_base = [normalizar_texto(item["texto"]) for item in base_local]
        faiss_db = create_faiss_index(textos_base)

        wiki_chunks = []
        for chunk in chunks_user[:2]:
            wiki_chunks.extend(buscar_artigos_wikipedia(chunk, max_artigos=2))

        if wiki_chunks:
            faiss_db.add_texts(wiki_chunks)
            print(
                f"[Wikipedia] {len(wiki_chunks)} chunks adicionados ao FAISS")

        suspeitos = []
        for chunk in chunks_user:
            resultados = faiss_db.similarity_search(chunk, k=1)
            if not resultados:
                continue

            emb_user = embedding_model.embed_query(chunk)
            emb_base = embedding_model.embed_query(resultados[0].page_content)
            score = util.cos_sim(emb_user, emb_base).item()

            if score > threshold:
                suspeitos.append({
                    "trecho_usuario": chunk,
                    "trecho_base": resultados[0].page_content,
                    "similaridade": round(score, 2)
                })

        percentual = len(suspeitos) / len(chunks_user) * 100
        return percentual, suspeitos

    except Exception as e:
        print(f"[Erro] {e}")
        return 0, [{"erro": str(e)}]
