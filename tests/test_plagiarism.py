from app.plagiarism import plagiarism_check


def test_plagiarism_check():
    texto_usuario = "machine learning é uma área da inteligência artificial"
    base_local = [{"texto": "machine learning é muito usado em IA"}]
    resultado = plagiarism_check(
        texto_usuario, base_local, threshold=0.5, top_k=3)

    assert "percentual_plagio_semantico" in resultado
    assert "percentual_plagio_lexico" in resultado
    assert isinstance(resultado["suspeitos_semantico"], list)
