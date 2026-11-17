from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.ingest import IngestRequest
from app.services.extraction import extract_url_content


async def ingest_content(
    payload: IngestRequest,
    db: Session
) -> Item:

    if payload.source_type == "note":
        content = payload.content
        title = payload.title or "Untitled Note"
        source_url = None

    else:
        source_url = str(payload.url)

        extracted_title, content = await extract_url_content(
            source_url
        )

        title = payload.title or extracted_title

    item = Item(
        title=title,
        source_type=payload.source_type,
        source_url=source_url,
        raw_content=content,
        status="completed"
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
