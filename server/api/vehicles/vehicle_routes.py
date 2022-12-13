from server.api.vehicles import vehicle_controller
from fastapi import  Depends, WebSocket
from fastapi import APIRouter, HTTPException
from server.db_config import get_db
from sqlalchemy.orm import Session
from http import HTTPStatus

vehicle_router = APIRouter()
  
@vehicle_router.get("/lookup/{vin}")
async def get_vehicle_by_vin(vin:str, db:Session = Depends(get_db)):
    try:
        return await vehicle_controller.get_vehicle_by_vin(db=db, vin= vin)
    except Exception as e:
        raise HTTPException( status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"{e}")

@vehicle_router.delete("/remove/{vin}")
async def delete_vehicle_by_vin(vin:str, db:Session = Depends(get_db)):
    try:
        return vehicle_controller.delete_vehicle_by_vin(db=db, vin=vin)
    except Exception as e:
        raise HTTPException( status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"{e}")

@vehicle_router.websocket("/export")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await vehicle_controller.export_database_cache(websocket)
    except Exception as e:
        raise HTTPException( status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
    