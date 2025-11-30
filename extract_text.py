import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import zipfile
import io

def extract_text(file_path, file_type):
    try:
        # -------------------------
        # PDF
        # -------------------------
        if file_type == 'pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += (page.extract_text() or '') + '\n'

            text = text.strip()

            # If almost empty → run OCR
            if len(text) < 100:
                from pdf2image import convert_from_path
                images = convert_from_path(file_path)
                ocr_text = ''
                for img in images:
                    ocr_text += pytesseract.image_to_string(img)
                text += '\n' + ocr_text

            return text.strip()

        # -------------------------
        # DOCX
        # -------------------------
        elif file_type == 'docx':
            doc = Document(file_path)
            text = '\n'.join(p.text for p in doc.paragraphs).strip()

            if len(text) < 100:
                # Extract images inside DOCX
                ocr_text = ''
                with zipfile.ZipFile(file_path, 'r') as docx_zip:
                    for f in docx_zip.namelist():
                        if f.startswith("word/media/"):
                            img_data = docx_zip.read(f)
                            img = Image.open(io.BytesIO(img_data))
                            ocr_text += pytesseract.image_to_string(img)

                text += "\n" + ocr_text

            return text.strip()

        # -------------------------
        # IMAGE
        # -------------------------
        elif file_type == 'image':
            img = Image.open(file_path)
            return pytesseract.image_to_string(img).strip()

        # -------------------------
        # TEXT FILE (NOTEPAD)
        # -------------------------
        elif file_type == "txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()

        else:
            return "Error: Unsupported file type."

    except Exception as e:
        return f"Error extracting text: {str(e)}"
