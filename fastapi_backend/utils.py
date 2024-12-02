from sqlalchemy.orm import Session
from models import Enrollment
from database import SessionLocal

def add_enrollments(user_id, course_ids):
    session: Session = SessionLocal()
    try:
        for course_id in course_ids:
            enrollment = Enrollment(user_id=user_id, course_id=course_id)
            session.add(enrollment)
        session.commit()
        print(f"Added enrollments for user {user_id}: {course_ids}")
    except Exception as e:
        session.rollback()
        print(f"Failed to add enrollments: {e}")
    finally:
        session.close()
