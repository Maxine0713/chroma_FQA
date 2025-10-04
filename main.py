import os
import uvicorn
from app import app  

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

UVICORN_RELOAD = os.getenv("UVICORN_RELOAD", "False").lower() == "true"
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=UVICORN_RELOAD)
