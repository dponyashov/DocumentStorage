from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from db_dir.config import _Config

Base = declarative_base()
engine = create_engine(_Config.DB_URL)

Base.metadata.create_all(engine)
Base.metadata.bind = engine