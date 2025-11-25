from pydantic import BaseModel


class QueryRequest(BaseModel):
    """
    Request schema for the /query endpoint.

    Why separate file?
    - Keeps main.py cleaner.
    - Easy to reuse types across modules.
    - Better organization as project grows.
    """
    question: str


class QueryResponse(BaseModel):
    """
    Response schema for the /query endpoint.

    We can extend this later with:
    - sources: list of documents used
    - scores: retrieval scores
    - model_name: which LLM answered, etc.
    """
    answer: str
    info: str

class DocumentCreate(BaseModel):
    """
    Request body for creating a new document.

    Why separate schema?
    - It clearly defines what the client must send.
    - We can later add fields (e.g., tags, metadata) without breaking internals.
    """
    title: str
    content: str


class DocumentInfo(BaseModel):
    """
    Response model for listing / returning documents.

    We intentionally only return a preview of the content to keep responses small.
    """
    id: int
    title: str
    content_preview: str