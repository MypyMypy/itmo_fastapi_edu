from fastapi import FastAPI, HTTPException
from app.models import Base, engine
from app.schemas import TermCreate, TermResponse
from sqlalchemy.orm import Session
from app.crud import get_all_terms, create_term, get_term_by_name, update_term, delete_term

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/", summary="Главная страница", description="Возвращает приветственное сообщение.")
def read_root():
    return {"message": "Welcome to the Glossary API!"}

@app.get("/terms", response_model=list[TermResponse], tags=["Terms"])
def get_terms():
    with Session(engine) as session:
        return get_all_terms(session)

@app.post("/terms", response_model=TermResponse)
def add_term(term: TermCreate):
    with Session(engine) as session:
        existing_term = get_term_by_name(session, term.name)
        if existing_term:
            raise HTTPException(status_code=400, detail="Term already exists")
        return create_term(session, term)

@app.put("/terms/{term_name}", response_model=TermResponse)
def edit_term(term_name: str, term: TermCreate):
    with Session(engine) as session:
        existing_term = get_term_by_name(session, term_name)
        if not existing_term:
            raise HTTPException(status_code=404, detail="Term not found")
        return update_term(session, term_name, term)

@app.delete("/terms/{term_name}")
def remove_term(term_name: str):
    with Session(engine) as session:
        existing_term = get_term_by_name(session, term_name)
        if not existing_term:
            raise HTTPException(status_code=404, detail="Term not found")
        delete_term(session, term_name)
        return {"message": "Term deleted successfully"}

