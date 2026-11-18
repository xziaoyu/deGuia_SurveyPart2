from fastapi import FastAPI
from sqlmodel import Session , select
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine
from fastapi.middleware.cors import CORSMiddleware

from models import Surveynimo

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:3000",  # React development server
    "https://example.com",    # Production frontend
    "*"
] # Define allowed origins (domains that can access your API)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allow these origins
    allow_credentials=True,       # Allow cookies, authentication headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)



@app.get("/")
async def root():
    return {"message": "HEYY"}


@app.get("/surveynimo/{id}")
async def read_employee(id):
    with Session(engine) as session:
        print(id,'--------------------------------------------------------------')
        surveynimo = session.get(Surveynimo, id)
        return {"message": surveynimo}
    

@app.post("/surveynimo")
async def root(surveynimo  : Surveynimo):

    with Session(engine) as session:
        session.add(surveynimo)
        session.commit()
        session.refresh(surveynimo)
        return {"message": surveynimo}
 