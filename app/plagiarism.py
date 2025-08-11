from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from sentence_transformers import util
from app.utils import normalizar_texto
import wikipedia
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

wikipedia.set_lang("pt")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def chunk_text(texto, chunk_size=300, overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(texto)


def create_faiss_index(docs):
    return FAISS.from_texts(docs, embedding_model)


def search_wikipedia_articles(termo_busca, max_artigos=3):
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
                            f"[Wikipedia] Artigo '{titulo}' carregado ({lang}), tamanho: {len(conteudo)} chars"
                        )

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


def lexical_similarity_search(chunks_user, textos_base, threshold=0.7):
    suspeitos = []
    if not textos_base or not chunks_user:
        return suspeitos

    vectorizer = TfidfVectorizer().fit(textos_base + chunks_user)
    tfidf_base = vectorizer.transform(textos_base)
    tfidf_user = vectorizer.transform(chunks_user)

    for i, user_vec in enumerate(tfidf_user):
        cosine_similarities = cosine_similarity(user_vec, tfidf_base).flatten()
        max_sim_idx = cosine_similarities.argmax()
        max_sim = cosine_similarities[max_sim_idx]

        if max_sim > threshold:
            suspeitos.append({
                "trecho_usuario": chunks_user[i],
                "trecho_base": textos_base[max_sim_idx],
                "similaridade": round(float(max_sim), 2)
            })

    return suspeitos


def plagiarism_check(user_text, base_local, threshold=0.5, top_k=5):
    try:
        user_text = normalizar_texto(user_text)
        chunks_user = chunk_text(user_text)
        if not chunks_user:
            return {
                "percentual_plagio_semantico": 0,
                "percentual_plagio_lexico": 0,
                "suspeitos_semantico": [{"erro": "Texto muito curto para análise"}],
                "suspeitos_lexico": []
            }

        textos_base_raw = [item["texto"] for item in base_local]
        textos_base_chunks = []
        for texto in textos_base_raw:
            texto_norm = normalizar_texto(texto)
            textos_base_chunks.extend(chunk_text(texto_norm))

        faiss_db = create_faiss_index(textos_base_chunks)

        
        wiki_chunks = []
        for chunk in chunks_user[:5]:
            wiki_chunks.extend(search_wikipedia_articles(chunk, max_artigos=2))

        if wiki_chunks:
            faiss_db.add_texts(wiki_chunks)
            print(
                f"[Wikipedia] {len(wiki_chunks)} chunks adicionados ao FAISS")

        suspeitos_semantico = []
        for chunk in chunks_user:
            resultados = faiss_db.similarity_search(chunk, k=1)
            if not resultados:
                continue

            emb_user = embedding_model.embed_query(chunk)
            emb_base = embedding_model.embed_query(resultados[0].page_content)
            score = util.cos_sim(emb_user, emb_base).item()

            if score > threshold:
                suspeitos_semantico.append({
                    "trecho_usuario": chunk,
                    "trecho_base": resultados[0].page_content,
                    "similaridade": round(score, 4)
                })

        suspeitos_semantico = sorted(
            suspeitos_semantico, key=lambda x: x["similaridade"], reverse=True
        )[:top_k]
        percentual_semantico = (
            len(suspeitos_semantico) / len(chunks_user)) * 100

        suspeitos_lexico = lexical_similarity_search(
            chunks_user, textos_base_chunks, threshold
        )
        suspeitos_lexico = sorted(
            suspeitos_lexico, key=lambda x: x["similaridade"], reverse=True
        )[:top_k]
        percentual_lexico = (len(suspeitos_lexico) / len(chunks_user)) * 100

        return {
            "percentual_plagio_semantico": percentual_semantico,
            "percentual_plagio_lexico": percentual_lexico,
            "suspeitos_semantico": suspeitos_semantico,
            "suspeitos_lexico": suspeitos_lexico,
        }

    except Exception as e:
        print(f"[Erro] {e}")
        return {
            "percentual_plagio_semantico": 0,
            "percentual_plagio_lexico": 0,
            "suspeitos_semantico": [{"erro": str(e)}],
            "suspeitos_lexico": []
        }
