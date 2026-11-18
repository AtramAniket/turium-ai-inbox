from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemResponse


router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):

    statement = (
        select(Item)
        .order_by(Item.created_at.desc())
    )

    items = db.scalars(statement).all()

    return items
