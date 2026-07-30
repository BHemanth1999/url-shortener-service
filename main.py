from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import router
from app.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="URL Shortener Service",
    description="A scalable URL shortener with APIs, persistence, and analytics",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
