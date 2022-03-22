import os
from sqlalchemy.orm import sessionmaker,  Session
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load database connection URI from .env
load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")

if not DATABASE_URI:
    raise Exception("DATABASE_URI not provided in environment")

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

# Alternatively data could be access via providers (as done in opencdms wrapper but assumed legacy)

# from opencdms.provider.climsoft import Climsoft4Provider
# from opencdms.provider.opencdms import OpenCDMSProvider, ProviderConfig

# climsoft_provider = Climsoft4Provider()
# stations = climsoft_provider.list(db_session, 'Station')
