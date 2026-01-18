import os
from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DocxLoader
from loaders.ppt_loader import PPTLoader
from loaders.excel_loader import ExcelLoader

def get_loader(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return PDFLoader()
    elif ext in [".docx"]:
        return DocxLoader()
    elif ext in [".ppt", ".pptx"]:
        return PPTLoader()
    elif ext in [".xls", ".xlsx"]:
        return ExcelLoader()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
