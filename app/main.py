# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database
from pydantic import BaseModel

app = FastAPI()

class Course(BaseModel):
    course: str
    course_name: str
    course_summary: str
    image_url: str

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + PostgreSQL"}

@app.post("/posts/")
def create_post(post: Course, db: Session = Depends(get_db)):
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
