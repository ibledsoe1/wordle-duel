"""FastAPI app for managing wordle-duel endpoints"""

# I think I need this later
from contextlib import asynccontextmanager

from fastapi import FastAPI

tags_metadata = [
    {
        "name":"General",
        "description":"Basic application information and health checks.",
    },
]

app = FastAPI(
    title="Wordle Duel API",
    description="Manage Wordle Duel endpoints.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

@app.get("/", tags=["General"], summary="API landing point/introduction")
def read_root() -> dict[str, str]:
    # Introduce the API
    return {"message":"Wordle Duel API"}

@app.get("/health", tags=["General"], summary="Check API health")
def health_check() -> dict[str, str]:
    # Confirm API process is running.
    return {"status":"healthy"}