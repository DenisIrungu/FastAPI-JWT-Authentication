from sqlalchemy import Column,String,Integer
from database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True)
    username=Column(String(50), unique=True)
    hashed_password=Column(String(255))