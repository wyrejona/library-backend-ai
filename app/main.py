from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import Query
# from app.ai.embeddings import embed_text  <-- REMOVED (handled inside retriever now)
from app.ai.retrieval import retriever      # <-- UPDATED (use the class instance)
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
    # 1. Search directly using the retriever instance
    # Note: retriever.search() takes the raw string, embeds it, and finds matches.
    chunks = retriever.search(query.query)
    
    if not chunks:
        return {"answer": "I could not find this information in the library materials."}

    # 2. Prepare Context
    # Add a separator so the LLM knows where one chunk ends and another begins
    context = "\n\n---\n\n".join(chunks)

    # 3. Generate Answer
    answer = ask_llm(context, query.query)
    
    return {"answer": answer}
