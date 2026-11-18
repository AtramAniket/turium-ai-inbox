
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class CitationResponse(BaseModel):
    title: str
    item_id: str
    source_url: str
    chunk_index: int
    content: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]
