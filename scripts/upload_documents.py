from pathlib import Path

from app.pdf_reader import extract_text_from_pdf
from app.chunking import create_chunks
from app.embeddings import create_embedding
from app.vector_store import add_document_chunk


DOCUMENTS = [
    {
        "path": "documents/graduation_project_book.pdf",
        "document_type": "graduation_book",
        "document_name": "Graduation Project Book",
    },
    {
        "path": "documents/contract_SH-06A.pdf",
        "document_type": "contract",
        "document_name": "Contract SH-06A",
    },
    {
        "path": "documents/contract_SH-06B_SH-06C.pdf",
        "document_type": "contract",
        "document_name": "Contract SH-06B and SH-06C",
    },
]


def upload_document(document):
    pdf_path = Path(document["path"])

    print(f"\nProcessing: {document['document_name']}")

    pages = extract_text_from_pdf(pdf_path)
    chunks = create_chunks(pages)

    print(f"Pages found: {len(pages)}")
    print(f"Chunks created: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        chunk_id = (
            f"{document['document_type']}_"
            f"{pdf_path.stem}_"
            f"page_{chunk['page']}_"
            f"chunk_{index}"
        )

        embedding = create_embedding(chunk["text"])

        metadata = {
            "document_type": document["document_type"],
            "document_name": document["document_name"],
            "page": chunk["page"],
        }

        add_document_chunk(
            chunk_id=chunk_id,
            text=chunk["text"],
            embedding=embedding,
            metadata=metadata,
        )

        print(f"Uploaded chunk {index + 1}/{len(chunks)}")


def main():
    for document in DOCUMENTS:
        upload_document(document)

    print("\nAll documents uploaded successfully.")


if __name__ == "__main__":
    main()