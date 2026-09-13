import os
import chromadb

CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_data")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="shepheard_documents"
)

def add_document_chunk(
    chunk_id,
    text,
    embedding,
    metadata
):
    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def search_documents(query_embedding, n_results=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results