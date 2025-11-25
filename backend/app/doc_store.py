from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Document:
    """
    Internal representation of a document stored in our system.

    Why dataclass?
    - Lightweight, built into Python (no extra dependency).
    - Type-safe and easy to extend later (e.g., add 'metadata', 'created_at', etc.).
    """
    id: int
    title: str
    content: str


# In-memory "database" for now.
# Later, this will be replaced by a real vector DB and/or persistent storage.
_DOCS: List[Document] = []
_NEXT_ID: int = 1


def add_document(title: str, content: str) -> Document:
    """
    Add a new document to the in-memory store.

    For now:
    - We just append to a list.

    Later:
    - We'll also compute embeddings and write to a vector store.
    - We'll track this document via DVC/MLflow.
    """
    global _NEXT_ID

    doc = Document(id=_NEXT_ID, title=title, content=content)
    _DOCS.append(doc)
    _NEXT_ID += 1
    return doc


def list_documents() -> List[Document]:
    """
    Return all documents in the store.

    Later:
    - Might support pagination, filters, user-specific docs, etc.
    """
    return list(_DOCS)


def get_all_documents() -> List[Document]:
    """
    Alias for list_documents for clarity in RAG logic.
    """
    return list_documents()


def get_document_by_id(doc_id: int) -> Optional[Document]:
    """
    Get a document by its ID.
    """
    for doc in _DOCS:
        if doc.id == doc_id:
            return doc
    return None
