# file_parser.py
import docx
import fitz  # PyMuPDF for PDFs

def extract_text(file):
    ext = file.name.split('.')[-1].lower()

    if ext == "txt":
        return file.read().decode("utf-8")

    elif ext == "docx":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif ext == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])

    else:
        return "❌ Unsupported file format. Please upload PDF, DOCX, or TXT."
