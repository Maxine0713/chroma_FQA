from fastapi import FastAPI
from router import embedding, faq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# 設置跨域請求
origins = [
    "http://localhost:3030",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Disposition"],  # 暴露 Content-Disposition 標頭
)
# Middleware 來自動記錄所有 API


@app.get("/")
def root():
    return {"msg": "Chroma + FastAPI running!"}


# 設定路由
app.include_router(embedding.router)
app.include_router(faq.router)
