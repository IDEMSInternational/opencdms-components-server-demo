import os
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load database connection URI from .env
load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")

engine: Engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(engine)

Base = declarative_base()


async def get_session() -> Session:
    """
    Api dependency to provide database session to a request
    """

    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
