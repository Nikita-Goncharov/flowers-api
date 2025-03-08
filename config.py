import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    @property
    def DB_NAME():
        return os.getenv("DB_NAME")
    
    @property
    def DB_HOST():
        return os.getenv("DB_HOST")
    
    @property
    def DB_PORT():
        return os.getenv("DB_PORT")
    
    @property
    def DB_USER():
        return os.getenv("DB_USER")
    
    @property
    def DB_PASSWORD():
        return os.getenv("DB_PASSWORD")
    
config = Config()