from pydoc import text
from sentence_transformers import SentenceTransformer
from vector_store.base import TextVectorStore
from config import MODEL_NAME, TOP_K

# 模型與儲存初始化（可依需求調整）
model_name = MODEL_NAME
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

    return True


def search_in_store(query: str, top_k: int = TOP_K):
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
    # 確認有此id,再刪除
    exist = text_store.collection.get(ids=[id])
    if not exist["ids"]:
        return False
    text_store.delete(ids=[id])
    return True


def clear_store():
    # 刪除之前，需取得所有 id
    all_ids = text_store.collection.get()["ids"]
    if all_ids:
        text_store.collection.delete(ids=all_ids)
    return True


def count_store():
    count = text_store.collection.count()
    return count


def list_store():
    all_docs = text_store.collection.get()
    output = []
    for i in range(len(all_docs["ids"])):
        output.append(
            {
                "id": all_docs["ids"][i],
                "text": all_docs["documents"][i],
                "metadata": all_docs["metadatas"][i],
            }
        )
    return output
