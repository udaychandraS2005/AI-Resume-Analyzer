from pypdf import PdfReader
from pypdf.errors import PdfReadError
 
 
class ResumeExtractionError(Exception):
    """Raised when a resume PDF cannot be read or parsed."""
 
 
def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF resume.
 
    Raises ResumeExtractionError with a user-friendly message instead of
    letting low-level pypdf exceptions (corrupted file, wrong format,
    password-protected PDF, etc.) crash the app.
    """
 
    try:
        reader = PdfReader(pdf_file)
    except (PdfReadError, Exception) as exc:
        raise ResumeExtractionError(
            "This file could not be read as a PDF. It may be corrupted, "
            "not a real PDF, or saved in an unsupported format."
        ) from exc
 
    if getattr(reader, "is_encrypted", False):
        raise ResumeExtractionError(
            "This PDF is password-protected. Please upload an "
            "unprotected PDF."
        )
 
    resume_text = ""
 
    for page in reader.pages:
        try:
            text = page.extract_text()
        except Exception as exc:
            raise ResumeExtractionError(
                "This PDF could not be fully read. Try re-exporting it "
                "from your word processor."
            ) from exc
 
        if text:
            resume_text += text + "\n"
 
    return resume_text
