from sentence_transformers import SentenceTransformer
from embeddings.vector_store import TextVectorStore


# 模型與儲存初始化（可依需求調整）
model_name = "paraphrase-multilingual-MiniLM-L12-v2"
collection_name = "text_collection"
model = SentenceTransformer(model_name)
text_store = TextVectorStore(collection_name=collection_name)


def add_doc_to_store(id: str, text: str, metadata: dict = {}):
    embedding = model.encode(text, normalize_embeddings=True).tolist()
    if not text or not id:
        return {"status": "error", "msg": "id and text are required."}
    text_store.add(
        embeddings=[embedding],
        documents=[text],
        ids=[id],
        metadatas=[metadata],
    )

    return {"status": "ok", "msg": f"doc {id} added."}


def search_in_store(query: str, top_k: int = 3):
    embedding = model.encode(query, normalize_embeddings=True).tolist()
    results = text_store.query(
        query_embedding=embedding,
        top_k=top_k,
    )
    output = []
    for i in range(len(results["ids"][0])):
        distances = results["distances"][0]
        similarities = []
        for d in distances:
            if d is not None:
                similarities.append(1 - d)
            else:
                similarities.append(None)
        output.append(
            {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distances": distances[i],
                "similarities": similarities[i],
            }
        )
    return output


def delete_from_store(id: str):
    text_store.delete(ids=[id])
    return {"status": "ok", "msg": f"doc {id} deleted."}


def clear_store():
    text_store.collection.delete()
    return {"status": "ok", "msg": "All docs deleted."}


def count_store():
    count = text_store.collection.count()
    return {"status": "ok", "count": count}
