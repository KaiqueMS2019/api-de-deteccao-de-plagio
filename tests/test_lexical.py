from app.plagiarism import lexical_similarity_search


def test_lexical_similarity_search():
    chunks_user = ["gato preto dorme no sofá"]
    textos_base = ["gato preto descansa no sofá", "cachorro corre no parque"]
    suspeitos = lexical_similarity_search(
        chunks_user, textos_base, threshold=0.5)
    assert len(suspeitos) > 0
