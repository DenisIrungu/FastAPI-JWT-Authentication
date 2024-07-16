from fastapi import FastAPI,status,Depends,HTTPException
import model
from database import engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import auth
from auth import get_current_user 

app= FastAPI()
app.include_router(auth.router)

#Binding and creating all the models
model.Base.metadata.create_all(bind=engine)

#Dependencies for our datase
def get_db():
    db= SessionLocal()
    try:
        yield db

    finally:
        db.close()

#Dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency= Annotated[dict, Depends(get_current_user)]

#API endpoint that just fetches the user
@app.get("/",status_code=status.HTTP_200_OK)
async def user(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentcation failed")
    return {"User":user}