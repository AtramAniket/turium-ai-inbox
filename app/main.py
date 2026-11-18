from app.api.ingest import router as ingest_router
from app.api.query import router as query_router
from app.api.items import router as items_router

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
	init_db()
	yield



app = FastAPI(
    title="Turium AI Knowledge Inbox",
    description="A knowledge management API powered by RAG.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingest_router)
app.include_router(items_router)
app.include_router(query_router)