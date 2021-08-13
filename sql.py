from getpass import getpass
from mysql.connector import connect, Error
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename="logfile.log")

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")


def create_connection(database):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = connect(
            host="localhost",
            user=USER,
            password=PASSWORD,
            database=database,
        )
        return conn
    except Error as e:
        logging.error(e)


def execute_sql(conn, sql, params=None):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :param params
    :return:
    """
    with conn.cursor(buffered=True) as cursor:
        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            return cursor
        except Error as e:
            logging.error(e)


def create_database():
    sql = """CREATE DATABASE if not exists PasswordManager"""
    conn = None
    try:
        with connect(
                host="localhost",
                user=USER,
                password=PASSWORD,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
    except Error as e:
        logging.error(e)


def create_table(conn):
    sql = """CREATE TABLE if not exists passwords (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    );"""
    execute_sql(conn, sql)
    conn.commit()


def add_password(conn, name, password):
    """
    Create a new password into the passwords table
    :param conn:
    :param password:
    :return: password id
    """
    sql = '''INSERT INTO passwords(name, password)
             VALUES(%s, %s)'''
    cur = execute_sql(conn, sql, (name, password))
    conn.commit()
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
        qs.append(f"{k}=%s")
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
    sql = f"SELECT password FROM passwords WHERE name=%s"
    cur = execute_sql(conn, sql, (name,))
    password = cur.fetchone()
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
             WHERE id = %s'''

    try:
        execute_sql(conn, sql, values)
        conn.commit()
    except Error as e:
        logging.error(e)


def delete(conn, id):
    """
    delete password
    :param conn:
    :param id: row id
    :return:
    """
    sql = "DELETE FROM passwords WHERE id=?"
    execute_sql(conn, sql, (id,))
    conn.commit()

