"""
DSN x BCT Hackathon 3.0 — Task B
Recommendation Agent · FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.routers import recommend, health
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 DSN x BCT Task B — Recommendation Agent starting...")
    logger.info(f"   Model : {settings.MODEL_NAME}")
    logger.info(f"   Items : catalog loaded")
    yield
    logger.info("🛑 Shutting down...")


app = FastAPI(
    title="DSN x BCT — Task B: Recommendation Agent",
    description=(
        "LLM-powered personalised recommendation agent. "
        "Handles cold-start, cross-domain, and multi-turn scenarios. "
        "Built for the DSN × Bluechip Tech Hackathon 3.0."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(health.router, tags=["Health"])
app.include_router(recommend.router, prefix="/api/v1", tags=["Recommendations"])


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
