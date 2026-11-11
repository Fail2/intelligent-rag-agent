from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

BASE_DIR = Path(__file__).resolve().parent.parent
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


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Check application health.

    Function: health_check
    Args: None
    Returns:
        dict[str, str]: Application health status.
    """
    return {"status": "healthy"}
