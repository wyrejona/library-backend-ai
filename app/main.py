from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import Query
from app.ai.embeddings import embed_text
from app.ai.retrieval import search
from app.ai.llm import ask_llm

app = FastAPI(title="Library AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later for WordPress
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask(query: Query):
    query_embedding = embed_text(query.query)
    chunks = search(query_embedding)
    context = "\n\n".join(chunks)
    answer = ask_llm(context, query.query)
    return {"answer": answer}
