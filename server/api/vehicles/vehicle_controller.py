from sqlalchemy.orm import Session
from server.models.vehicle import Vehicle
from server.schemas.vehicle_schema import VehicleBase,VehicleAdd, VehicleDelete
from server.app_config import appConfig
from server.db_config import engine
from fastapi import WebSocket
import requests, json
import pandas as pd

async def get_vehicle_by_vin(db:Session, vin:str):
    
    cached_vin_data = db.query(Vehicle).filter(Vehicle.vin == vin).first()
    
    if(cached_vin_data):
        cached_vin_data.cached_result = True
        return cached_vin_data

    fetched_vin_data = await __get_vehicle_data_from_vpic_api(vin)
    
    if(fetched_vin_data):
        vehicleAdd = VehicleAdd(vin = vin, 
                        make = fetched_vin_data['Make'],
                        model=fetched_vin_data['Model'], 
                        model_year=fetched_vin_data['Model Year'],
                        body_class=fetched_vin_data['Body Class'])
        
        new_vin_data = __add_vehicle_data(db, vehicleAdd)
        new_vin_data.cached_result = False
        return new_vin_data

def delete_vehicle_by_vin(db:Session, vin:str):
    delete_status = db.query(Vehicle).filter(Vehicle.vin == vin).delete()
    db.commit()
    return VehicleDelete(vin= vin, cached_delete_success= bool(delete_status))

async def export_database_cache(websocket: WebSocket):
    file_name = 'vehicle.parquet'
    
    __export_sqlite_to_parquet_file(file_name)
    parquet_file = open(file_name, 'rb')
    
    await websocket.accept()
    await websocket.send_bytes(parquet_file.read())
    await websocket.close()
    
    
# Private Methods
    
async def __get_vehicle_data_from_vpic_api(vin):
    url = f"{appConfig.VPIC_DECODE_API}{vin}?format=json";
    res = requests.get(url)
    deserialized_json_data = json.loads(res.text)
    processed_vin_data = VehicleBase.convert_array_to_dictionary(deserialized_json_data['Results'])
    return processed_vin_data

def __add_vehicle_data(db:Session, vehicleAdd:VehicleAdd):
    new_vehicle =  Vehicle(vin=vehicleAdd.vin, 
                        make=vehicleAdd.make,
                        model=vehicleAdd.model, 
                        model_year=vehicleAdd.model_year,
                        body_class=vehicleAdd.body_class)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

def __export_sqlite_to_parquet_file(file_name:str):
    dataToParquet = pd.read_sql(f"SELECT * from {Vehicle.__tablename__ }", con=engine)
    dataToParquet.to_parquet(file_name, index=False)