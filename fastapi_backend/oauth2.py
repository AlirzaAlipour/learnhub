import os
from dotenv import load_dotenv
from fastapi import exceptions, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from typing import Optional
from jwt.exceptions import InvalidTokenError


load_dotenv()
  
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_access_token(token: str = Depends(oauth2_scheme)) -> Optional[int]:
    credentials_exception = exceptions.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = decode(token, PUBLIC_KEY, algorithms=["RS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    
    return user_id

