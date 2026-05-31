import io
import re
from pypdf import PdfReader
from docx import Document


class ParseError(Exception):
    """Raised when a file cannot be parsed."""


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _parse_txt(data: bytes) -> str:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1", errors="replace")
    return _normalize(text)


def _parse_docx(data: bytes) -> str:
    try:
        doc = Document(io.BytesIO(data))
    except Exception as e:
        raise ParseError(f"Could not read DOCX: {e}") from e
    return _normalize("\n".join(p.text for p in doc.paragraphs))


def _parse_pdf(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception as e:
        raise ParseError(f"Could not read PDF: {e}") from e
    return _normalize("\n".join(pages))


def parse(filename: str, data: bytes) -> str:
    """Parse resume bytes into normalized plain text. Dispatch by extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "txt":
        return _parse_txt(data)
    if ext == "docx":
        return _parse_docx(data)
    if ext == "pdf":
        return _parse_pdf(data)
    raise ParseError(f"Unsupported file type: .{ext}")
