# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# App modules (correct imports)
from app.schemas import Query
from app.ai.embeddings import embed_text
from app.ai.retrieval import search
from app.ai.llm import ask_llm

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="Library AI Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for WordPress domain in production
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."},
    )

@app.post("/ask")
@limiter.limit("5/minute")
def ask(query: Query, request: Request):
    query_embedding = embed_text(query.query)
    context_chunks = search(query_embedding)
    answer = ask_llm(context_chunks, query.query)
    return {"answer": answer}
