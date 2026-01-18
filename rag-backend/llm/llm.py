from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

# ------------------ Streaming LLM ------------------

def stream_llm(prompt: str):
    """
    Streams model output token-by-token.
    Defensive against empty / malformed responses.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = getattr(response, "text", None)

    if not text or not isinstance(text, str):
        return

    for token in text.split(" "):
        yield token + " "


# ------------------ Embeddings ------------------

def embed_text(text: str) -> list[float]:
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return response.embeddings[0].values


def embed_texts(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    """
    Optimized batching to avoid per-call overhead.
    """
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        response = client.models.embed_content(
            model="text-embedding-004",
            contents=batch
        )

        for emb in response.embeddings:
            embeddings.append(emb.values)

    return embeddings


# ------------------ Non-streaming call (optional) ------------------

def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text or ""
