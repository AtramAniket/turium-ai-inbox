from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import retrieve_relevant_chunks
from app.services.generation import generate_answer

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_knowledge_base(payload: QueryRequest):

    try:
        chunks = retrieve_relevant_chunks(payload.question)

        result = generate_answer(
            question=payload.question,
            retrieved_chunks=chunks,
        )

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process your question right now.",
        )
