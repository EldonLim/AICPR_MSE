# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

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

@app.post("/users/")
def create_user(name: str, db: Session = Depends(get_db)):
    user = models.User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/posts/")
def create_post(title: str, description: str, image_url: str, db: Session = Depends(get_db)):
    post = models.Post(title=title, description=description, image_url=image_url)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
