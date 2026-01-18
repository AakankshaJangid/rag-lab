from fastapi.responses import StreamingResponse
from chat.history import save_message, get_recent_messages
from llm.llm import embed_text, stream_llm
from vectorstore.mongodb import similarity_search
from sentence_transformers import CrossEncoder
from hashlib import md5
import json

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# ------------------ Helpers ------------------

def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def is_valid_answer(answer: str, sources: list) -> bool:
    if not answer.strip():
        return False
    if not sources:
        return False
    return True


def build_memory_block(session_id: str, user_id: str) -> str:
    """
    Fetch last N user messages and inject as conversational memory.
    """
    history = get_recent_messages(
        session_id=session_id,
        user_id=user_id,
        limit=5
    )

    if not history:
        return ""

    return "\n".join(f"- {m}" for m in history)


# ------------------ Main RAG ------------------

def retrieve_and_stream(
    session_id: str,
    query: str,
    user_id: str,
    k: int = 5,
):
    # 1️⃣ Save user message
    save_message(session_id, user_id, "user", query)

    # 2️⃣ Embed query
    query_embedding = embed_text(query)

    # 3️⃣ Vector search (user filter ready)
    docs = similarity_search(
        query_embedding=query_embedding,
        k=k,user_id=user_id
    )
    if not docs:
        def empty_stream():
            yield "No relevant documents found. Please upload documents first."
        return StreamingResponse(empty_stream(), media_type="text/plain")


    

    # 4️⃣ Rerank
    pairs = [(query, d["text"]) for d in docs]
    scores = reranker.predict(pairs)

    reranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    top_docs = [d for _, d in reranked[:k]]

    # 5️⃣ Deduplicate chunks
    seen = set()
    deduped = []

    for d in top_docs:
        fp = md5(normalize(d["text"])[:300].encode()).hexdigest()
        if fp not in seen:
            seen.add(fp)
            deduped.append(d)

    # 6️⃣ Build context + sources
    context_blocks = []
    sources = []

    for i, d in enumerate(deduped):
        idx = i + 1
        context_blocks.append(f"[{idx}] {d['text']}")

        sources.append({
            "source": d.get("source", "unknown"),
            "chunk_type": d.get("chunk_type"),
            "page": d.get("page"),
            "preview": d["text"][:300],
        })

    context = "\n\n".join(context_blocks)
    memory = build_memory_block(session_id, user_id)

    # 7️⃣ Final prompt (with memory)
    prompt = f"""
You are a retrieval-augmented system.

Rules:
- Answer ONLY using the provided context
- Do NOT hallucinate
- Cite facts using [1], [2], etc
- Be concise

Conversation history:
{memory}

Context:
{context}

Question:
{query}
"""

    full_answer = ""

    # 8️⃣ Streaming generator
    def stream():
        nonlocal full_answer

        for token in stream_llm(prompt):
            full_answer += token
            yield token

        if is_valid_answer(full_answer, sources):
            yield "\n\n[[SOURCES]]\n"
            yield json.dumps(sources, ensure_ascii=False)

        save_message(session_id, user_id, "assistant", full_answer)

    return StreamingResponse(
        stream(),
        media_type="text/plain; charset=utf-8",
    )
