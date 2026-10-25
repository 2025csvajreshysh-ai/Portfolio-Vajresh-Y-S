from contextlib import asynccontextmanager
from pathlib import Path
from datetime import date
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Field, Session, create_engine, select

BASE = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE / 'contact.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Portfolio API",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE / "static"),
    name="static",
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE / "static" / "index.html")