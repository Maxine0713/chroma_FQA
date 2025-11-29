from app import app
import uvicorn
from config import HOST, PORT, UVICORN_RELOAD

if __name__ == "__main__":
    uvicorn.run("run:app", host=HOST, port=PORT, reload=UVICORN_RELOAD)
