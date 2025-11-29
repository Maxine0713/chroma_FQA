from fastapi import APIRouter
from vector_store.text import search_in_store, list_store
from schemas.schemas import SearchIn

router = APIRouter(prefix="/embedding", tags=["embedding"])


@router.get("/")
def all_embeddings():
    """
    列出目前向量資料庫中的所有文件。
    Returns:
        dict: {"status": "ok", "data": list of documents}
    """
    return {"status": "ok", "data": list_store()}


@router.post("/search/")
def search_embeddings(search: SearchIn):
    """
    以語意嵌入方式查詢資料庫，回傳最相關的 top_k 筆資料。
    Args:
        search (SearchIn): 查詢內容與 top_k 筆數
    Returns:
        dict: {"status": "ok", "data": list of search results}
    """
    output = search_in_store(query=search.query, top_k=search.top_k)

    return {"status": "ok", "data": output}
