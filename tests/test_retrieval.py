from app.retrieval import retrieve_relevant_documents


def test_retrieval_finds_relevant_documents():
    question = "What is the project delivery method?"

    results = retrieve_relevant_documents(question, n_results=3)

    assert len(results["documents"]) > 0
    assert len(results["documents"][0]) > 0