from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# ---------- Request & Response Schemas ----------

class QueryRequest(BaseModel):
    """
    This defines what the client must send to /query.

    Why?
    - Clear contract between frontend and backend.
    - FastAPI validates data automatically.
    - OpenAPI docs (Swagger UI) are generated from this.
    """
    question: str


class QueryResponse(BaseModel):
    """
    This defines what our API will return.

    Why?
    - Makes response predictable and documented.
    - Easy for frontend + monitoring + tests.
    """
    answer: str
    info: str


# ---------- FastAPI Application ----------

app = FastAPI(
    title="OSS RAG Assistant",
    description="Open-source LLM + RAG backend with FastAPI",
    version="0.1.0",
)

# ---------- CORS Middleware ----------

# In development, allow all origins. In production, restrict this to your frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # TODO: change to ["https://your-frontend.com"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Health Check Endpoint ----------

@app.get("/health")
def health_check():
    """
    Health endpoint.

    Why?
    - Kubernetes uses this URL to see if the container is healthy.
    - AWS load balancer & uptime monitors can ping this.
    - Prometheus alerting can depend on this being up.
    """
    return {"status": "ok"}


# ---------- Core RAG Query Endpoint (Stub For Now) ----------

@app.post("/query", response_model=QueryResponse)
def query_rag(payload: QueryRequest):
    """
    This will be our main RAG endpoint.

    Right now:
    - We return a dummy answer.

    Later:
    - We'll implement full RAG:
        1. Use an embedding model to embed payload.question
        2. Retrieve top-k relevant chunks from vector DB
        3. Build a prompt with context
        4. Call local open-source LLM
        5. Return answer + metadata (sources, scores, etc.)

    Why create a stub?
    - Let frontend already talk to backend (end-to-end “skeleton”).
    - We can add logging, monitoring, Docker, CI/CD around it early.
    - RAG implementation can be iterated without breaking API.
    """
    dummy_answer = f"You asked: '{payload.question}'. RAG is not implemented yet."
    info = "This is a placeholder. Soon this will run the full RAG pipeline over your documents."
    return QueryResponse(answer=dummy_answer, info=info)