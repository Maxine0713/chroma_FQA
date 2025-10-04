import json
from fastapi import APIRouter
from embeddings.utils import add_doc_to_store, count_store, clear_store

router = APIRouter(prefix="/faq", tags=["faq"])


@router.post("/add/all/")
def add_faq():
    # 先清空現有資料，再加入FAQ
    clear_store()
    # 讀取FAQ資料並加入向量庫
    faq_data = json.load(open("./faq.json", "r", encoding="utf-8"))
    for i, item in enumerate(faq_data):
        add_doc_to_store(
            id=f"faq_{i}",
            text=item.get("question"),
            metadata={"answer": item.get("answer")},
        )
    return {"status": "ok", "msg": "FAQ added."}


@router.post("/add/plus/")
def add_faq():
    # 在現有資料基礎上加入FAQ
    now_count = count_store()["count"]
    # 讀取FAQ資料並加入向量庫
    faq_data = json.load(open("./faq.json", "r", encoding="utf-8"))
    for i, item in enumerate(faq_data):
        add_doc_to_store(
            id=f"faq_{i+now_count}",
            text=item.get("question"),
            metadata={"answer": item.get("answer")},
        )
    return {"status": "ok", "msg": "FAQ added."}
