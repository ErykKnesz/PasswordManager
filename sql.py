import sqlite3
from sqlite3 import Error
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename="logfile.log")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        logging.error(e)
    return conn


def execute_sql(conn, sql, params=None):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :param params
    :return:
    """
    try:
        c = conn.cursor()
        if params is None:
            c.execute(sql)
        else:
            c.execute(sql, params)
        conn.commit()
        return c
    except Error as e:
        logging.error(e)


def create_table(conn):
    sql = """CREATE TABLE passwords (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    );"""
    execute_sql(conn, sql)


def add_password(conn, password):
    """
    Create a new password into the passwords table
    :param conn:
    :param password:
    :return: password id
    """
    sql = '''INSERT INTO passwords(name, password)
             VALUES(?,?)'''
    cur = execute_sql(conn, sql, password)
    return cur.lastrowid


def select_all(conn):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    sql = "SELECT * FROM passwords ORDER BY name"
    cur = execute_sql(conn, sql)
    rows = cur.fetchall()
    return rows


def select_passwords_where(conn, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param query: dict of attributes and values
    :return:
    """
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    sql = f"SELECT * FROM passwords WHERE {q}"
    cur = execute_sql(conn, sql, values)
    rows = cur.fetchall()
    return rows


def select_password(conn, name):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param name: name to which the password is assigned
    :return:
    """
    sql = f"SELECT FROM passwords WHERE name=?"
    cur = execute_sql(conn, sql, (name,))
    password = cur.fetchone()[2]
    return password


def update(conn, id, **kwargs):
    """
    update password
    :param conn:
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f''' UPDATE passwords
             SET {parameters}
             WHERE id = ?'''

    try:
        execute_sql(sql, values)
    except sqlite3.OperationalError as e:
        logging.ERROR(e)


def delete(conn, id):
    """
    delete password
    :param conn:
    :param id: row id
    :return:
    """
    sql = "DELETE FROM passwords WHERE id=?"
    execute_sql(sql, (id,))


if __name__ == '__main__':
    conn = create_connection(r"database.db")
    conn.close()