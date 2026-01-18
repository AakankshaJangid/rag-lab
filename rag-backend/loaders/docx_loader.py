from docx import Document
from loaders.base_loader import BaseLoader

class DocxLoader(BaseLoader):

    def load(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
