import os
from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class AppConfig(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION")
    SQLITE_DATABASE: str = os.getenv("SQLITE_DATABASE")
    VPIC_DECODE_API: str = os.getenv("VPIC_DECODE_API")
    HOST:str = os.getenv("HOST")
    PORT:int = os.getenv("PORT")

appConfig = AppConfig()