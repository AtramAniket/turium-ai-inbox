
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ItemResponse(BaseModel):
    id: UUID
    title: str
    source_type: str
    source_url: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
