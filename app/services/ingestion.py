
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.ingest import IngestRequest
from app.services.extraction import extract_url_content
from app.services.chunking import chunk_text
from app.services.embedding import generate_embeddings_for_chunks
from app.services.vector_store import store_chunks


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
        status="processing"
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    try:
        chunks = chunk_text(content)

        embeddings = generate_embeddings_for_chunks(chunks)

        store_chunks(
            item_id=str(item.id),
            title=item.title,
            source_type=item.source_type,
            source_url=item.source_url,
            chunks=chunks,
            embeddings=embeddings,
        )

        item.status = "completed"
        db.commit()
        db.refresh(item)

    except Exception:
        item.status = "failed"
        db.commit()
        raise

    return item
