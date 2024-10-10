from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database_setup import engine
from models import Document, Archiv

DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_doc_by_id(doc_id):
    doc = session.query(Document).filter_by(id=doc_id).one()
    return doc


def get_doc_list(is_deleted=False):
    if is_deleted:
        return session.query(Document).all()
    return session.query(Document).filter_by(is_deleted=is_deleted).all()

def save_new_doc(title, content):
    newDoc = Document(title=title, content=content)
    session.add(newDoc)
    session.commit()

def save_doc(id_doc, title, content):
    updateDoc = session.query(Document).filter_by(id=id_doc).one()

    newArch = Archiv()
    newArch.id_doc = updateDoc.id
    newArch.ts = datetime.now()
    newArch.title = updateDoc.title
    newArch.content = updateDoc.content

    session.add(newArch)

    updateDoc.title = title
    updateDoc.content = content

    session.commit()

def delete_doc(doc_id):
    updateDoc = session.query(Document).filter_by(id=doc_id).one()
    updateDoc.is_deleted = True
    session.commit()

def get_version(doc_id, last=False):
    if last:
        last_vers = session.query(Archiv).filter_by(id_doc=doc_id).order_by(desc(Archiv.ts)).first()
        return last_vers
    vers = session.query(Archiv).filter_by(id_doc=doc_id).order_by(Archiv.ts).first()
    return vers


def get_arch_list_by_doc(doc_id):
    archs = session.query(Archiv).filter_by(id_doc=doc_id).all()
    return archs


def get_arch_by_id(arch_id):
    arch = session.query(Archiv).filter_by(id=arch_id).one()
    return arch