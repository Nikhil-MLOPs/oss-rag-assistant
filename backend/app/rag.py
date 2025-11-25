# from typing import Tuple


# def run_rag(question: str) -> Tuple[str, str]:
#     """
#     This function represents our RAG pipeline.

#     Why have it as a separate module?
#     - All retrieval + LLM logic lives here.
#     - main.py stays a thin API layer.
#     - Easier to unit test & instrument with MLflow + Prometheus.

#     For now:
#     - It's a dummy implementation.
#     Later:
#     - We'll add:
#         * document store (Chroma/Qdrant)
#         * embeddings
#         * prompt building
#         * LLM calls
#     """
#     # Simulate that we used some "knowledge base"
#     fake_context = (
#         "This is a placeholder RAG context. "
#         "In the future, this will be built from your uploaded documents."
#     )

#     answer = (
#         f"I received your question: '{question}'.\n\n"
#         f"Right now, I don't have a real knowledge base wired in, "
#         f"but soon I'll search your documents and answer using RAG."
#     )

#     info = f"DEBUG CONTEXT (fake): {fake_context}"

#     return answer, info

from typing import Tuple, Optional, List

from .doc_store import get_all_documents, Document


def _simple_retrieve(question: str, documents: List[Document]) -> Optional[Document]:
    """
    Naive retrieval: choose the document with the highest word overlap.

    Why?
    - No external dependencies (good for initial skeleton).
    - Gives us a "shape" similar to real retrieval (input -> ranked docs).

    This will be replaced with:
    - Embeddings
    - Vector similarity search (Chroma/Qdrant)
    """
    if not documents:
        return None

    q_words = set(question.lower().split())
    best_doc = None
    best_score = 0

    for doc in documents:
        doc_words = set(doc.content.lower().split())
        score = len(q_words.intersection(doc_words))
        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc


def run_rag(question: str) -> Tuple[str, str]:
    """
    Entry point for our RAG logic.

    Current behavior:
    1. Pull all documents from the in-memory store.
    2. Retrieve the "most relevant" one via naive overlap.
    3. Build an answer string that mentions the chosen document.

    Later:
    - We'll:
        * Use embeddings + vector DB for retrieval
        * Possibly combine multiple documents
        * Call a real LLM to generate the answer
        * Log performance/evals with MLflow
    """
    docs = get_all_documents()

    if not docs:
        answer = (
            "I don't have any documents yet. "
            "Please upload some via the /docs endpoint, then ask again."
        )
        info = "No documents in store. RAG pipeline could not run."
        return answer, info

    best_doc = _simple_retrieve(question, docs)

    if best_doc is None:
        answer = (
            "I looked through your documents but couldn't find anything obviously relevant.\n"
            "Once we upgrade to real embeddings + vector search, this will improve."
        )
        info = "Naive retrieval found no overlapping words."
        return answer, info

    # Use a simple snippet from the chosen doc as "context"
    snippet = best_doc.content[:400]

    answer = (
        f"I selected a document titled: '{best_doc.title}' as the most relevant.\n\n"
        f"Here's a relevant snippet:\n\n"
        f"{snippet}\n\n"
        f"(Later, this snippet will be passed to a real LLM to generate a richer answer.)"
    )

    info = f"Selected document ID: {best_doc.id} with naive word-overlap retrieval."

    return answer, info
