import chromadb
import os
from config import (
    CHROMA_IMAGE_PATH,
    CHROMA_TEXT_PATH,
    TOP_K,
)

persist_dir = os.getenv("PERSIST_DIR", "/tmp/data")
os.makedirs(persist_dir, exist_ok=True)


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            # 明確指定使用 cosine 距離，避免distances大於1
        )

    def add(self, ids, embeddings, metadatas=None, documents=None):
        self.collection.add(
            ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents
        )

    def query(self, query_embedding, top_k=TOP_K):
        raw_result = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )
        return raw_result

    def delete(self, ids):
        self.collection.delete(ids=ids)


class TextVectorStore(VectorStore):
    def __init__(self, collection_name: str):
        super().__init__(persist_dir=CHROMA_TEXT_PATH, collection_name=collection_name)


class ImageVectorStore(VectorStore):
    def __init__(self, collection_name: str):
        super().__init__(persist_dir=CHROMA_IMAGE_PATH, collection_name=collection_name)
