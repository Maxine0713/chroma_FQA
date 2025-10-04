from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ===== 路徑設定 =====
# 直接使用專案根目錄下的 data 資料夾
PERSIST_ROOT = Path(__file__).parents[1] / "data"

DEFAULT_TEXT_COLLECTION = "text_collection"
DEFAULT_IMAGE_COLLECTION = "image_collection"

# 設定 Chroma 路徑放在可寫的 /tmp 目錄
CHROMA_TEXT_PATH = PERSIST_ROOT / "chroma_text"
CHROMA_IMAGE_PATH = PERSIST_ROOT / "chroma_image"

# 其他參數
TOP_K = 5
ALPHA = 0.5
