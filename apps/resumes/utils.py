import os
import docx
from pdfminer.high_level import extract_text

def extract_text_from_file(file_path):
    """
    Extracts text from PDF or DOCX file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == '.pdf':
            text = extract_text(file_path)
        elif ext == '.docx':
            doc = docx.Document(file_path)
            text = " ".join([para.text for para in doc.paragraphs])
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""
        
    return text.strip()
