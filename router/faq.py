from calendar import c
import json
from fastapi import APIRouter, HTTPException
from vector_store.text import (
    add_doc_to_store,
    count_store,
    clear_store,
    delete_from_store,
)
from config import JSON_FILE_PATH
from schemas.schemas import FAQItem, FAQWithId

router = APIRouter(prefix="/faq", tags=["faq"])


def read_faq_json():
    """讀取 faq.json 並回傳 FAQ 列表"""
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def write_faq_json(faq_list=list[FAQWithId]):
    """將 FAQ 列表寫入 faq.json"""
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(faq_list, f, ensure_ascii=False, indent=2)


@router.get("/")
def list_faq():
    """
    列出目前 FAQ 資料庫中的所有 FAQ 條目。
    Returns:
        list: FAQ 條目列表，每筆包含 id、question、answer
    """
    faq_data = json.load(open("./faq.json", "r", encoding="utf-8"))
    return faq_data


@router.get("/count/")
def count_faq():
    """
    取得目前 FAQ 資料庫中的 FAQ 筆數。
    Returns:
        dict: {"status": "ok", "count": int}
    """
    return {"status": "ok", "count": count_store()}


@router.post("/init/")
def init_faq():
    """
    初始化 FAQ 資料庫，清空現有 FAQ 並以資料夾內的faq.json檔案進行向量資料庫創建。
    Returns:
        dict: {"status": "ok", "msg": "FAQ initialized."}
    """
    if count_store() > 0:
        clear_store()
    faq_list = read_faq_json()
    for item in faq_list:
        add_doc_to_store(
            id=str(item.get("id")),
            text=item.get("question"),
            metadata={"answer": item.get("answer")},
        )
    return {"status": "ok", "msg": "FAQ initialized."}


@router.post("/append/")
def append_faq(faq_list: list[FAQItem]):
    """
    追加 FAQ 至現有 FAQ 資料庫，不清空原有資料。
    可傳入 FAQ list，會自動生成遞增 id。
    Args:
        faq_list (List[FAQItem], optional): FAQ 格式列表
    Returns:
        dict: {"status": "ok", "msg": "FAQ added."}
    """

    # 合併到原有 json
    old_list = read_faq_json()
    # 取得現有最大 id
    max_id = max(item["id"] for item in old_list)
    print("max_id", max_id)
    add_faq = [faq.model_dump() for faq in faq_list]
    # 為新 FAQ 補上 id
    for idx, item in enumerate(add_faq):
        item["id"] = max_id + idx + 1
    write_faq_json(old_list + add_faq)
    for faq in add_faq:
        add_doc_to_store(
            id=str(faq["id"]),
            text=faq["question"],
            metadata={"answer": faq["answer"]},
        )
    return {"status": "ok", "msg": f"FAQ added {len(add_faq)}."}


@router.delete("/{faq_id}/")
def delete_faq(faq_id: int):
    """
    根據 FAQ id 刪除指定 FAQ，並同步更新 faq.json。
    Args:
        faq_id (int): FAQ 的唯一 id
    Returns:
        dict: {"status": "ok", "msg": "doc {id} deleted."}
    """
    # 刪除資料庫
    result = delete_from_store(id=str(faq_id))
    if result is False:
        HTTPException(status_code=404, detail=f"doc {id} not found.")
    # 刪除 json 檔案中的 FAQ
    faq_list = read_faq_json()
    new_list = [item for item in faq_list if item.get("id") != faq_id]
    write_faq_json(new_list)
    return {"status": "ok", "msg": f"doc {faq_id} deleted."}
