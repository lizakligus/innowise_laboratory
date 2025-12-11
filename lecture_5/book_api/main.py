from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os

app = FastAPI(title="Book API") #create app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'books.db')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
Base.metadata.create_all(bind=engine)

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: Optional[int] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def create_book(book: Book, db: Session = Depends(get_db)):
    db_book = BookDB(title=book.title, author=book.author, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    book.id = db_book.id
    return book

@app.get("/books/", response_model=List[Book])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(BookDB).all()
    return books

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: Book, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_update.title
    book.author = book_update.author
    book.year = book_update.year
    db.commit()
    db.refresh(book)
    return Book(id=book.id, title=book.title, author=book.author, year=book.year)

@app.get("/books/search/", response_model=List[Book])
def search_books(
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        db: Session = Depends(get_db)
):
    query = db.query(BookDB)

    if title:
        query = query.filter(BookDB.title.contains(title))
    if author:
        query = query.filter(BookDB.author.contains(author))
    if year:
        query = query.filter(BookDB.year == year)

    books = query.all()
    return books

@app.get("/")
def read_root():
    return {"message": "Welcome to Book API", "docs": "http://127.0.0.1:8000/docs"}