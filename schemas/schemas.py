from pydantic import BaseModel

from config import TOP_K


class SearchIn(BaseModel):
    """
    查詢嵌入資料的請求格式。
    Attributes:
        query (str): 查詢文字
        top_k (int): 回傳前 k 筆最相關結果
    """

    query: str
    top_k: int = TOP_K


class FAQItem(BaseModel):
    """
    FAQ 項目的資料格式。
    Attributes:
        question (str): FAQ 問題
        answer (str): FAQ 答案
    """

    question: str
    answer: str


class FAQWithId(FAQItem):
    """
    包含 ID 的 FAQ 項目資料格式。
    Attributes:
        id (int): FAQ 唯一識別碼
        question (str): FAQ 問題
        answer (str): FAQ 答案
    """

    id: int
