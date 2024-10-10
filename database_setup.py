from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from config import DB_URL

Base = declarative_base()
engine = create_engine(DB_URL)

Base.metadata.create_all(engine)
Base.metadata.bind = engine