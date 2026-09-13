from app.pdf_reader import extract_text_from_pdf


def test_graduation_book_can_be_read():
    pdf_path = "documents/graduation_project_book.pdf"

    pages = extract_text_from_pdf(pdf_path)

    assert len(pages) > 0
    assert pages[0]["text"].strip() != ""


def test_contract_sh_06a_can_be_read():
    pdf_path = "documents/contract_SH-06A.pdf"

    pages = extract_text_from_pdf(pdf_path)

    assert len(pages) > 0
    assert pages[0]["text"].strip() != ""


def test_contract_sh_06b_sh_06c_can_be_read():
    pdf_path = "documents/contract_SH-06B_SH-06C.pdf"

    pages = extract_text_from_pdf(pdf_path)

    assert len(pages) > 0
    assert pages[0]["text"].strip() != ""