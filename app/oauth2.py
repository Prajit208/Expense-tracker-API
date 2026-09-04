from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from. import database,models,schemas
from datetime import datetime, timezone,timedelta
from fastapi import HTTPException,Depends,status
import os
from dotenv import load_dotenv

# *loading environment variable

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# ^pass login route
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode=data.copy() # ?copy to avoid overriding original
    expire=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire}) # ?adding an expire key value pair 
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

    
def verify_access_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str= payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)   
        return token_data
    except JWTError:
        raise credentials_exception
        
    
def get_current_user(token: str =Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user credentials")
    token=verify_access_token(token, credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
        
    return user



'''
# ~ oauth2.py handles creating and verifying access tokens.

A token is a signed string containing the user's id and an expiry time.
It's signed with a secret key known only to the server, so the server can trust that a valid 
token wasn't forged or tampered with.

create_access_token builds and signs a new token after login. 
verify_access_token decodes an incoming token and checks the signature and expiry are valid. 
get_current_user uses the verified token's user id to fetch the actual user from the database, 
so protected routes know exactly who's making the request.

'''
