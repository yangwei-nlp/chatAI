import uvicorn
from fastapi import FastAPI
from backend.insert_file import insert_router
from backend.rag import rag_router
from backend.search import search_router

app = FastAPI()

app.include_router(insert_router)
app.include_router(rag_router)
app.include_router(search_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
