from fastapi import FastAPI
from server.api.vehicles.vehicle_routes import vehicle_router
from server.app_config import appConfig
from server.db_config import engine
from server.db_config import Base

def include_router(app):
	app.include_router(vehicle_router)

def start_application():
	Base.metadata.create_all(bind=engine)
	app = FastAPI(title=appConfig.PROJECT_NAME, description=appConfig.PROJECT_DESCRIPTION)
	include_router(app)
	return app 

app = start_application()