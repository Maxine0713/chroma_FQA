
## 目錄結構

```
app.py                  # FastAPI 主程式，API 路由整合
run.py                  # 啟動伺服器 (Uvicorn)
faq.json                # FAQ 資料 (JSON 格式)
config.py               # 路徑與參數設定
router/                 # API 路由
  ├─ faq.py             # FAQ 管理 API
  └─ embedding.py       # 語意查詢 API
vector_store/           # 向量儲存相關程式
  ├─ base.py            # 向量儲存基礎類別
  └─ text.py            # 文字向量儲存類別與查詢工具
schemas/
  └─ schemas.py         # Pydantic 資料結構定義
data/chroma_text/       # Chroma 向量資料庫
```

## 1. 安裝與虛擬環境

1. 安裝 Python 3.11 或以上版本
2. 建議建立虛擬環境：
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. 安裝依賴套件：
    ```bash
    pip install -r requirements.txt
    ```

## 2. 設定說明
- 複製 `.env.example` 為 `.env`，並根據需求修改參數：
- 路徑與參數請參考 `config`

## 3. 執行方式
啟動 FastAPI 伺服器：
```bash
python run.py
```

## API 說明
啟動後可直接瀏覽自動產生的 API 文件：
- 互動式 Swagger UI： [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc 文件： [http://localhost:8000/redoc](http://localhost:8000/redoc)


### FAQ 資料格式
請參考 `faq.json`，每筆資料包含：
```json
{
  "id": 1,
  "question": "有提供退貨服務嗎？",
  "answer": "是的，我們提供7天內無條件退貨服務，請確保商品未拆封且保留原包裝。"
}
```



## 其他
- FAQ 新增/刪除會同步更新資料庫與 faq.json
- 進入向量資料庫的id，必須為字串型別
