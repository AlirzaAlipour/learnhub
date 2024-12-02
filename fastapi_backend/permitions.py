from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from oauth2 import verify_access_token
from models import Enrollment
from database import get_db

def verify_permission(course_id: int, user_id: int = Depends(verify_access_token) , db: Session = Depends(get_db)) -> bool:
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()
    
    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to access this course."
        )
    return True