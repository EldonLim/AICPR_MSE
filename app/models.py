# app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    course = Column(String, index=True)
    course_name = Column(String, index=True)
    course_summary = Column(String, index=True)
    image_url = Column(String, index=True)