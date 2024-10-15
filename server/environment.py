import os
import re

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Environment:
    def __init__(self):
        self.app_env = os.getenv('DJANGO_ENV') or "development"
        env_debug = os.getenv('DEBUG') == "True"
        self.is_debug = self.app_env == "development" and env_debug
        self.local_postgres_url = os.getenv('LOCAL_POSTGRES_URL')
        self.clouddatabase_url = os.getenv('DATABASE_URL')
        self.secret_key = os.getenv('SECRET_KEY')
    
    def db_config(self):
        port = "5432"
        db_url = self.clouddatabase_url if self.app_env == "production" else self.local_postgres_url

        if not db_url:
            raise ValueError("Database URL is not set for the current environment.")

        regex = r"postgres://(.*?):(.*?)@(.*?)/(.*)"
        match = re.match(regex, db_url)

        if not match:
            raise ValueError("Invalid database URL format. Expected format: postgres://username:password@host/dbname")

        user, password, host, db_name = match.groups()
        
        if self.is_debug:
            print(f"user: {user}, password: {password}, host: {host}, db_name: {db_name}")
        
        return {
            "NAME": db_name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
    
    def is_production(self):
        return self.app_env == "production"

config = Environment()