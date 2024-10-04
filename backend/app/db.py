# db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os


# Get database URI from environment variables
def get_db_session():
    database_uri = os.getenv(
        "DATABASE_URI", "mysql+aiomysql://todo_user:todo_pass@database:3306/cbc_todo"
    )
    engine = create_async_engine(database_uri, echo=True)

    # Creating async sessionmaker
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    return AsyncSessionLocal
