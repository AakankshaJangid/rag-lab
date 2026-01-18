from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from ingestion.ingestion import ingest_file
from retrieval.retrieval import retrieve_and_stream
from auth.deps import get_current_user
from pydantic import BaseModel

app = FastAPI(title="rag_lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Ingest ----------------

@app.post("/ingest-file")
async def ingest_file_api(
    file: UploadFile = File(...),
    chunk_type: str = "recursive",
    user_id: str = Depends(get_current_user),  # 🔐 secured
):
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        ingest_file(temp_path, chunk_type,user_id)
    finally:
        os.remove(temp_path)

    return {"status": "file ingested", "user_id": user_id}


# ---------------- Query ----------------

class QueryRequest(BaseModel):
    session_id: str
    query: str
    k: int = 5


@app.post("/query")
def query_rag(
    body: QueryRequest,
    user_id: str = Depends(get_current_user),
):
    return retrieve_and_stream(
        session_id=body.session_id,
        query=body.query,
        k=body.k,
        user_id=user_id,
    )

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)