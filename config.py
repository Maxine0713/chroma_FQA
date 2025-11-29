from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
# 伺服器設定
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", 8000))
UVICORN_RELOAD = os.getenv("UVICORN_RELOAD", "False").lower() == "true"

# FAQ JSON 檔案路徑
JSON_FILE_PATH = Path(
    os.getenv("JSON_FILE_PATH", Path(__file__).parents[1] / "faq.json")
)

# 直接使用專案根目錄下的 data 資料夾
PERSIST_ROOT = Path(os.getenv("PERSIST_ROOT", Path(__file__).parents[1] / "data"))


# Chroma 路徑
CHROMA_TEXT_PATH = Path(os.getenv("CHROMA_TEXT_PATH", PERSIST_ROOT / "chroma_text"))
CHROMA_IMAGE_PATH = Path(os.getenv("CHROMA_IMAGE_PATH", PERSIST_ROOT / "chroma_image"))

# 其他參數
TOP_K = int(os.getenv("TOP_K", 5))

# 向量模型名稱
MODEL_NAME = os.getenv("MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
