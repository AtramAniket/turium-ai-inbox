from app.api.ingest import router as ingest_router
from app.api.query import router as query_router
from app.api.items import router as items_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-inbox-frontend-3qoh.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ingest_router, prefix=settings.api_v1_prefix,)
app.include_router(items_router, prefix=settings.api_v1_prefix,)
app.include_router(query_router, prefix=settings.api_v1_prefix,)