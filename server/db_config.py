from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from server.app_config import appConfig
from sys import modules


if(appConfig.TEST_ENV in modules.keys()):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./vehicles.db"
    
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()