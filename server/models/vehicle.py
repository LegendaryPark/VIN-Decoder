from sqlalchemy import Column, String, Boolean
from server.db_config import Base

class Vehicle(Base):
    __tablename__ = 'vehicle'
    
    vin= Column(String, primary_key=True, index= True)
    make= Column(String)
    model= Column(String)
    model_year= Column(String)
    body_class= Column(String)
    

