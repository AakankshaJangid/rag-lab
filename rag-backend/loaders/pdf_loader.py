import fitz  # PyMuPDF
from loaders.base_loader import BaseLoader

class PDFLoader(BaseLoader):

    def load(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        text = []

        for page in doc:
            text.append(page.get_text())

        return "\n".join(text)
