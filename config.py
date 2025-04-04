
from pydantic_settings import BaseSettings

from typing import Optional

class Settings(BaseSettings):
    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = '.env', '.env.prod'

    BACKEND_URL: str 
    EMAIL_URL :str
    BASE_URL: str 
    PASS_CODE : str
    EMAIL : str
    HOST : str
    DATABASE : str
    USER : str
    PASSWORD : str 
    PORT : str
    MAIN_PORT : int




