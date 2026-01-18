from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def insert_documents(docs: list[dict]):
    if not docs:
        print("No documents to insert!")
        return
    try:
        collection.insert_many(docs)
        print(collection)
        print(f"Inserted {len(docs)} documents.")
    except Exception as e:
        print("Error inserting documents:", e)


def similarity_search(
    query_embedding: list,
    k: int,
    user_id: str,
    doc_ids: list[str] | None = None,
    num_candidates: int = 100,
):
    if not query_embedding:
        return []

    # ensure embedding is float
    query_embedding = [float(x) for x in query_embedding]

    filter_query = {"user_id": user_id}
    if doc_ids:
        filter_query["doc_id"] = {"$in": doc_ids}

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "k": k,
                "limit": max(k, num_candidates),
                "filter": filter_query,
                "numCandidates": max(num_candidates, k)  # ✅ always ≥ k
            }
        },
        {
            "$project": {
                "text": 1,
                "source": 1,
                "_score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    print("🔎 QUERY USER_ID:", user_id)
    print(
        "📦 DOC COUNT FOR USER:",
        collection.count_documents({"user_id": user_id})
    )
    try:
        results = list(collection.aggregate(pipeline))
        return results
    except Exception as e:
        print("Vector search failed:", e)
        return []
