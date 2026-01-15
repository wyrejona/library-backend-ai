import faiss
import pickle
import numpy as np
from pathlib import Path

DATA_DIR = Path("app/data")

index = faiss.read_index(str(DATA_DIR / "faiss.index"))
chunks = pickle.load(open(DATA_DIR / "chunks.pkl", "rb"))

def search(query_embedding, top_k=4):
    D, I = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )
    return [chunks[i] for i in I[0]]