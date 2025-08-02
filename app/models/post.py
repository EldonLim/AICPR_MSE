# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    course = Column(String, index=True)
    course_name = Column(String, index=True)
    course_summary = Column(String, index=True)
    course_description = Column(String, index=True)
    number_of_semester = Column(String, index=True)
    course_url = Column(String, index=True)
    themes = Column(ARRAY(String), index=True)
    tags = Column(ARRAY(String), index=True)
