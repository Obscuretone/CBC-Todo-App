import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Base settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # Database configuration
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "mysql://todo_user:todo_pass@127.0.0.1:3307/cbc_todo"
    )

    # Redis configuration
    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379/0")

    AZURE_STORAGE_QUEUE_URI = os.getenv(
        "AZURE_STORAGE_QUEUE_URI", "http://localhost:10001/devstoreaccount1"
    )

    # Sanic specific settings
    SANIC_DEBUG = os.getenv("SANIC_DEBUG", "False") == "True"
    SANIC_AUTO_RELOAD = os.getenv("SANIC_AUTO_RELOAD", "True") == "True"
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "http://localhost:3000")
