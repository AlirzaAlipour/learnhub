from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: int | None = None


class CheckEnrollment(BaseModel):
    
    user_id : int 
    course_id : int