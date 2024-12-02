from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    user_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, primary_key=True)