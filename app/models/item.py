from typing import Optional

from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Item(Base):

	__tablename__="items"

	id: Mapped[UUID] = mapped_column(
		SQLAlchemyUUID(as_uuid=True),
		primary_key=True,
		default=uuid4
	)

	title: Mapped[str] = mapped_column(
		String,
		nullable=False
	)

	source_type: Mapped[str] = mapped_column(
		String,
		nullable=False
	)

	source_url: Mapped[Optional[str]] = mapped_column(
		String,
		nullable=True
	)

	raw_content: Mapped[str] = mapped_column(
		Text,
		nullable=False
	)

	status: Mapped[str] = mapped_column(
		String,
		nullable=False,
		default="processing"
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now()
	)
