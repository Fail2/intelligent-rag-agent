from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
CHECKPOINT_DB_PATH = BASE_DIR / "data" / "checkpoints.sqlite"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage the SQLite checkpointer lifecycle.

    Function: lifespan
    Args:
        app (FastAPI): FastAPI application instance.
    Returns:
        AsyncIterator[None]: Application lifespan context.
    """
    async with AsyncSqliteSaver.from_conn_string(
        str(CHECKPOINT_DB_PATH)
    ) as checkpointer:
        app.state.checkpointer = checkpointer
        yield


app = FastAPI(
    title="Intelligent RAG Agent",
    description="An intelligent RAG agent with LangGraph orchestration.",
    version="0.1.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_frontend():
    """Serve the chat interface.

    Function: serve_frontend
    Args: None
    Returns:
        FileResponse: Frontend HTML page.
    """
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health_check():
    """Check application health.

    Function: health_check
    Args: None
    Returns:
        dict: Application health status.
    """
    return {"status": "healthy"}
