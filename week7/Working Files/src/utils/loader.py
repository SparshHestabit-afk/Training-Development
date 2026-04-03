import os
import pandas as pd
from pypdf import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())
    return text

def load_text_files():
    text_path = os.path.join(RAW_DIR, "txt")
    documents = []

    if not os.path.exists(text_path):
        print(f"Directory {text_path} does not exist.")
        return documents
    
    for file in os.listdir(text_path):
        if file.endswith(".txt"):
            with open(os.path.join(text_path, file), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append({
                    "text": clean_text(text),
                    "metadata": {
                        "source": file,
                        "type": "txt"
                    }
                })

    return documents

def load_pdfs():
    pdf_path = os.path.join(RAW_DIR, "pdf")
    documents = []

    if not os.path.exists(pdf_path):
        print(f"Directory {pdf_path} does not exist.")
        return documents
    
    for file in os.listdir(pdf_path):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(pdf_path, file))

            for page_number, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text:
                    continue

                documents.append({
                    "text": clean_text(text),
                    "metadata": {
                        "source": file,
                        "page_number": page_number + 1,
                        "type": "pdf"
                    }
                })
    return documents

def load_csvs():
    csv_path = os.path.join(RAW_DIR, "csv")
    documents = []

    if not os.path.exists(csv_path):
        print(f"Directory {csv_path} does not exist.")
        return documents
    
    for file in os.listdir(csv_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(csv_path, file))

            documents.append({
                "text": clean_text(df.to_string(index=False)),
                "metadata": {
                    "source": file,
                    "type": "csv"
                }
            })
    return documents

def load_docx():
    docx_path = os.path.join(RAW_DIR, "docx")
    documents = []

    if not os.path.exists(docx_path):
        print(f"Directory {docx_path} does not exist.")
        return documents
    
    for file in os.listdir(docx_path):
        if file.endswith(".docx"):
            from docx import Document
            doc = Document(os.path.join(docx_path, file))

            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            documents.append({
                "text": clean_text("\n".join(full_text)),
                "metadata": {
                    "source": file,
                    "type": "docx"
                }
            })
    return documents

def load_documents():
    documents = []
    documents.extend(load_text_files())
    documents.extend(load_pdfs())
    documents.extend(load_csvs())
    documents.extend(load_docx())
    return documents