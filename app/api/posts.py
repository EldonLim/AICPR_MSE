# app/main.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import post as Model
from .. import database
from pydantic import BaseModel
from fastapi import HTTPException

router = APIRouter()

class Course(BaseModel):
    course: str
    course_name: str
    course_summary: str
    image_url: str

class CourseUpdate(BaseModel):
    course: Optional[str] = None
    course_name: Optional[str] = None
    course_summary: Optional[str] = None
    image_url: Optional[str] = None

Model.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_post(post: Course, db: Session = Depends(get_db)):
    post = Model.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Model.Post).all()
    return posts

@router.patch("/")
def update_post(courseCode: str, update_data: CourseUpdate, db: Session = Depends(get_db)):
    post = db.query(Model.Post).filter(Model.Post.course == courseCode).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = update_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(post, key, value) 

    db.commit()
    db.refresh(post)
    return post

@router.delete("/")
def delete_post(courseCode: str, db: Session = Depends(get_db)):
    post = db.query(Model.Post).filter(Model.Post.course == courseCode).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return {"detail": f"Post with courseCode '{courseCode}' deleted successfully."}