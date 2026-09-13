from app.pdf_reader import extract_text_from_pdf
from app.chunking import create_chunks


def test_graduation_book_can_be_chunked():
    pdf_path = "documents/graduation_project_book.pdf"

    pages = extract_text_from_pdf(pdf_path)
    chunks = create_chunks(pages)

    assert len(chunks) > 0
    assert chunks[0]["text"].strip() != ""
    assert "page" in chunks[0]