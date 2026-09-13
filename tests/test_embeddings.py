from app.embeddings import create_embedding


def test_text_can_be_embedded():
    text = "The project delivery method is Design-Bid-Build."

    embedding = create_embedding(text)

    assert embedding is not None
    assert len(embedding) > 0