from app.plagiarism import create_faiss_index

def test_create_faiss_index():
    docs = ["texto exemplo", "outro texto"]
    index = create_faiss_index(docs)
    assert index is not None
