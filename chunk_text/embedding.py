import ollama
import numpy as np


def ollama_embedding(texts: list[str], embed_model, **kwargs) -> np.ndarray:
    embed_text = []
    ollama_client = ollama.Client(**kwargs)
    for text in texts:
        data = ollama_client.embeddings(model=embed_model, prompt=text)
        embed_text.append(data["embedding"])

    return embed_text


