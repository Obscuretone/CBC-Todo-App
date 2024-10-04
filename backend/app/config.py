import os


# TODO: Move all the configs here.
class Config:
    # MySQL Database URI
    DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+aiomysql://todo_user:todo_pass@database:3306/cbc_todo"
    )

    # Redis URI
    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379/0")

    # Azure Queue Storage
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
