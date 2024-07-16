from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from model import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError



router = APIRouter(prefix="/auth",
                   tags=["auth"]
                   )
SECREAT_KEY= "Qh7h74jL9tHkYf2mP1sIc9wBtG5eJ3nWv0rXzU8qTs4zCd7rPjF"
ALGORITH= "HS256"

bcrypt_context= CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_bearer= OAuth2PasswordBearer(tokenUrl="auth/token")

class CreatUserRequest(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

#Dependency for our database

def get_db():
    db= SessionLocal()
    try: 
        yield db
    finally:
        db.close()
#Dependency injection
db_dependency= Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreatUserRequest):
    create_user_model= User(username= create_user_request.username,
                            hashed_password= bcrypt_context.hash(create_user_request.password))
    
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model= Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user= authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
    token= create_access_token(user.username, user.id,timedelta(minutes=20))
    return {"access_token":token, "token_type":"bearer"}

def authenticate_user(username:str,password:str, db):
    user= db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user 

def create_access_token(username:str,user_id:int,expired_delta:timedelta):
    encode ={"sub":username, "id": user_id}
    expired= datetime.utcnow() + expired_delta
    encode.update({"exp":expired})
    return jwt.encode(encode, SECREAT_KEY, algorithm=ALGORITH)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITH])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
            
    


