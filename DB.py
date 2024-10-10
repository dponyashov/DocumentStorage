import sqlite3
from datetime import datetime


def get_version(doc_id, desc=False):
    conn = open_db()
    cursor = conn.cursor()
    _SQL = 'SELECT * FROM t_archiv WHERE id_doc=? ORDER BY ts'
    if desc:
        _SQL += ' DESC'
    arch = cursor.execute(_SQL, (doc_id,)).fetchone()
    close_db(conn)
    return arch

def get_arch_list_by_doc(doc_id):
    conn = open_db()
    cursor = conn.cursor()
    archs = cursor.execute('SELECT * FROM t_archiv WHERE id_doc=?', (doc_id,)).fetchall()
    close_db(conn)
    return archs

def get_arch_by_id(arch_id):
    conn = open_db()
    cursor = conn.cursor()
    arch = cursor.execute('SELECT * FROM t_archiv WHERE id=?', (arch_id,)).fetchone()
    close_db(conn)
    return arch

def get_doc_by_id(doc_id):
    conn = open_db()
    cursor = conn.cursor()
    doc = cursor.execute('SELECT * FROM t_doc WHERE id=?', (doc_id,)).fetchone()
    close_db(conn)
    return doc


def get_doc_list(is_deleted=False):
    conn = open_db()
    cursor = conn.cursor()
    _SQL = 'SELECT * FROM t_doc'
    if not is_deleted:
        _SQL += ' WHERE is_deleted = 0'
    docs = cursor.execute(_SQL).fetchall()
    close_db(conn)
    return docs


def save_new_doc(title, content):
    conn = open_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO t_doc (title, content) VALUES (?, ?)', (title, content))
    close_db(conn)

def save_doc(id_doc, title, content):
    conn = open_db()
    cursor = conn.cursor()
    doc = cursor.execute('SELECT * FROM t_doc WHERE id=?', (id_doc,)).fetchone()
    cursor.execute('INSERT INTO t_archiv (id_doc, title, content, ts) VALUES (?, ?, ?, ?)',
                   (id_doc, doc['title'], doc['content'], datetime.now()))

    cursor.execute('UPDATE t_doc SET title=?, content=? WHERE id=?',(title, content, doc['id']))
    close_db(conn)


def delete_doc(doc_id):
    conn = open_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE t_doc SET is_deleted=? WHERE id=?',(1, doc_id,))
    close_db(conn)


def create_db():
    create_doc_table()
    create_archiv_table()

def create_doc_table():
    conn = open_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS t_doc (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT not null,
                                    content TEXT not null,
                                    is_deleted BOOLEAN default 0
                            )""")
    close_db(conn)


def create_archiv_table():
    conn = open_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS t_archiv (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        id_doc INTEGER,
                                        ts timestamp defaul timestamp,
                                        title TEXT not null,
                                        content TEXT not null
                                )""")
    close_db(conn)

def open_db():
    DB_NAME = 'docstorage.db'
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def close_db(conn):
    conn.commit()
    conn.close()


if __name__ =='__main_main':
    create_db()
