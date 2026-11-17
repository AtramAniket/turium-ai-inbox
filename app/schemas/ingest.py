from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator


class IngestRequest(BaseModel):
    source_type: Literal["note", "url"]

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    content: str | None = None

    url: HttpUrl | None = None

    @model_validator(mode="after")
    def validate_source(self):
        if self.source_type == "note":
            if not self.content or not self.content.strip():
                raise ValueError("Content is required for notes")

        elif self.source_type == "url":
            if not self.url:
                raise ValueError("URL is required for URL ingestion")

        return self
