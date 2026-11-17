from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.db.session import get_db
from app.schemas.ingest import IngestRequest
from app.schemas.item import ItemResponse
from app.services.ingestion import ingest_content


router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    payload: IngestRequest,
    db: Session = Depends(get_db)
):
    try:
        item = await ingest_content(payload, db)
        return item

    except httpx.HTTPError:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch the supplied webpage"
        )

    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during ingestion"
        )
