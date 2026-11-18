from app.api.ingest import router as ingest_router
from app.api.query import router as query_router

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
	init_db()
	yield



app = FastAPI(lifespan=lifespan)

app.include_router(ingest_router)
app.include_router(query_router)