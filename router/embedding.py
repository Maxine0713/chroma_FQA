from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from embeddings.vector_store import TextVectorStore
from embeddings.utils import add_doc_to_store, search_in_store, delete_from_store

router = APIRouter(prefix="/embedding", tags=["embedding"])


class DocIn(BaseModel):
    id: str
    text: str
    metadata: dict = {}


class SearchIn(BaseModel):
    query: str
    top_k: int = 3


class DeleteIn(BaseModel):
    id: str


@router.post("/add/")
def add_doc(doc: DocIn):
    return add_doc_to_store(id=doc.id, text=doc.text, metadata=doc.metadata)


@router.post("/search/")
def search_docs(search: SearchIn):
    return search_in_store(query=search.query, top_k=search.top_k)


@router.delete("/delete/")
def delete_doc(del_req: DeleteIn):
    return delete_from_store(id=del_req.id)
