from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF resume."""

    reader = PdfReader(pdf_file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    return resume_text