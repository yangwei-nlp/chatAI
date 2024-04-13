from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi import Body
import uvicorn, json, datetime
import torch
from sentence_transformers import SentenceTransformer

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE = 'cpu'

embeding_path = "/home/qilixin/文档/new_resource_platform/model/bge-base-zh-v1.5"
embedding_model = SentenceTransformer(embeding_path, device=DEVICE)

app = FastAPI()


@app.get("/")
async def func(content: str):
    vector = embedding_model.encode(content)
    vector = vector.flatten().tolist()
    return {'vector': vector}


class Req(BaseModel):
    queries: List[str]

@app.post("/embedding")
async def embed(req: Req):
    vectors = embedding_model.encode(req.queries)
    # return json.dumps({"embeddings": vectors.tolist()})
    return {"embeddings": vectors.tolist()}


if __name__ == '__main__':
    uvicorn.run(app="embedding:app", host='0.0.0.0', port=6000, workers=1, reload=True)
