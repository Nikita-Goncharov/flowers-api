import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    @property
    def DB_NAME(self):
        return os.getenv("DB_NAME")
    
    @property
    def DB_HOST(self):
        return os.getenv("DB_HOST")
    
    @property
    def DB_PORT(self):
        return os.getenv("DB_PORT")
    
    @property
    def DB_USER(self):
        return os.getenv("DB_USER")
    
    @property
    def DB_PASSWORD(self):
        return os.getenv("DB_PASSWORD")
    
config = Config()

db_config = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': config.DB_HOST,
                'port': config.DB_PORT,
                'user': config.DB_USER,
                'password': config.DB_PASSWORD,
                'database': config.DB_NAME,
                'minsize': 1,
                'maxsize': 1000,
            }
        }
    },
    'apps': {
        'models': {
            'models': [ 'models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'UTC'
}