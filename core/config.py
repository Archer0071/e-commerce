from pydantic import BaseSe
from decouple import config

class Settings(BaseSettings):
    DATABASE_URL = config("DATABASE_URL")
    

settings = Settings()