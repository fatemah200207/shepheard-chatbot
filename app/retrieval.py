from app.embeddings import create_embedding
from app.vector_store import search_documents


def retrieve_relevant_documents(question, n_results=5):
    question_embedding = create_embedding(question)

    results = search_documents(
        query_embedding=question_embedding,
        n_results=n_results
    )

    return results