from app.plagiarism import chunk_text


def test_chunk_text_division():
    texto = "A" * 1000
    chunks = chunk_text(texto, chunk_size=300, overlap=50)
    assert all(len(chunk) <= 300 for chunk in chunks)
    assert len(chunks) > 1
