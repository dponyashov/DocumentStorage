# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime

from db_dir.config import db_config

engine = create_engine(db_config.DB_URL)

# Base = declarative_base()
class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)
# Base.metadata.bind = engine

# Models
class Document(Base):
    __tablename__ = 't_doc'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(250), nullable=False)
    is_deleted = Column(Boolean, default=False)


class Archiv(Base):
    __tablename__ = 't_archiv'

    id = Column(Integer, primary_key=True)
    id_doc = Column(Integer, ForeignKey('t_doc.id'))
    ts = Column(DateTime, default=datetime.now())
    title = Column(String(100), nullable=False)
    content = Column(String(250), nullable=False)

if __name__== '__main__':
    Base.metadata.create_all(engine)