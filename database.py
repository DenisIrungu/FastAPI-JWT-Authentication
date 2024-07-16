from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_DATABASE = "mysql+pymysql://root:LayneLiam%4033@localhost:3306/FastAPIJWT"

engine= create_engine(URL_DATABASE)

Base= declarative_base()

SessionLocal= sessionmaker(bind=engine,autoflush=False, autocommit= False)