from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime
from database_setup import Base


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

