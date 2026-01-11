from sqlalchemy.orm import Session
from app.models import Term
from app.schemas import TermCreate

def get_all_terms(db: Session):
    return db.query(Term).all()

def create_term(db: Session, term: TermCreate):
    db_term = Term(name=term.name, description=term.description, link=term.link)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def get_term_by_name(db: Session, name: str):
    return db.query(Term).filter(Term.name == name).first()

def update_term(db: Session, name: str, term: TermCreate):
    db_term = db.query(Term).filter(Term.name == name).first()
    db_term.name = term.name
    db_term.description = term.description
    db_term.link = term.link
    db.commit()
    db.refresh(db_term)
    return db_term

def delete_term(db: Session, name: str):
    db_term = db.query(Term).filter(Term.name == name).first()
    db.delete(db_term)
    db.commit()
