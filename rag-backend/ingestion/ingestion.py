from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from llm.llm import embed_texts
from vectorstore.mongodb import insert_documents
from loaders.loader_factory import get_loader
from uuid import uuid4
import os
import re


# ----------------------------
# Paragraph Chunking
# ----------------------------
def paragraph_chunking(
    text: str,
    max_chars: int = 800
):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) <= max_chars:
            current += "\n\n" + para
        else:
            chunks.append(current.strip())
            current = para

    if current:
        chunks.append(current.strip())

    return chunks


# ----------------------------
# Section Chunking
# ----------------------------
def section_chunking(text: str):
    section_pattern = re.compile(
        r"(^\d+(\.\d+)*\s+.*$|^#+\s+.*$|^[A-Z][A-Z\s]{3,}$)",
        re.MULTILINE
    )

    matches = list(section_pattern.finditer(text))
    chunks = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunks.append(text[start:end].strip())

    return chunks if chunks else [text]


# ----------------------------
# Chunk Router
# ----------------------------
def chunk_text(
    text: str,
    chunk_type: str = "recursive"
):
    if chunk_type == "fixed":
        splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        return splitter.split_text(text)

    elif chunk_type == "recursive":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        return splitter.split_text(text)

    elif chunk_type == "paragraph":
        return paragraph_chunking(text)

    elif chunk_type == "section":
        return section_chunking(text)

    else:
        raise ValueError(f"Unsupported chunk_type: {chunk_type}")


# ----------------------------
# Text Ingestion
# ----------------------------
def ingest_text(
    text: str,
    chunk_type: str,
    user_id: str,
    source: str,
    doc_id: str,
):
    chunks = chunk_text(text, chunk_type)

    if not chunks:
        return

    # ⚡ BATCH EMBEDDINGS
    embeddings = embed_texts(chunks)

    docs = []
    for chunk, emb in zip(chunks, embeddings):
        docs.append({
            "text": chunk,
            "embedding": emb,
            "chunk_type": chunk_type,
            "user_id": user_id,   # 🔐 OWNERSHIP
            "doc_id": doc_id,     # 🧱 DOCUMENT
            "source": source,
        })

    insert_documents(docs)


# ----------------------------
# File Ingestion (ENTRY POINT)
# ----------------------------
def ingest_file(
    file_path: str,
    chunk_type: str,
    user_id: str,               # 🔐 REQUIRED
):
    loader = get_loader(file_path)
    text = loader.load(file_path)

    doc_id = str(uuid4())
    source = os.path.basename(file_path)

    ingest_text(
        text=text,
        chunk_type=chunk_type,
        user_id=user_id,
        source=source,
        doc_id=doc_id,
    )
