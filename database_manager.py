from getpass import getpass
from mysql.connector import connect, Error
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename="logfile.log")

DB_USER = os.environ.get('DB_USER') or input("Enter username: ")
PASSWORD = os.environ.get('PASSWORD') or getpass("Enter password: ")


class DatabaseManager:
    def __init__(self, database):
        self.connection = self._create_connection(database)

    def _create_connection(self, database):
        """ create a database connection to a Mysql database """
        try:
            conn = connect(
                host="localhost",
                user=DB_USER,
                password=PASSWORD,
                database=database,
            )
            return conn
        except Error as e:
            logging.error(e)

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def _execute_sql(self, sql, params=None):
        """ Execute sql
        :param sql: a SQL script
        :param params
        :return:
        """
        with self.connection.cursor(buffered=True) as cursor:
            try:
                if params is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, params)
                return cursor
            except Error as e:
                logging.error(e)

    def create_database(self):
        sql = """CREATE DATABASE if not exists PasswordManager"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
        except Error as e:
            logging.error(e)

    def create_table(self, table_name, columns):
        columns_with_types = [
            f" {column_name} {data_type}"
            for column_name, data_type in columns.items()
        ]
        sql = f"""CREATE TABLE if not exists {table_name} (
              {', '.join(columns_with_types)}
              );"""
        self._execute_sql(sql)
        self.connection.commit()

    def add_password(self, name, login, password):
        """
        Create a new password into the passwords table
        :param name:
        :param password:
        :param login:
        :return: password id
        """
        sql = """INSERT INTO passwords(name, login, password)
                 VALUES(%s, %s, %s)"""
        cur = self._execute_sql(sql, (name, login, password))
        self.connection.commit()
        return cur.lastrowid

    def select_all(self):
        """
        Query all rows in the table
        :return: query result
        """
        sql = "SELECT * FROM passwords ORDER BY name"
        cur = self._execute_sql(sql)
        return cur.fetchall()

    def select_passwords_where(self, **query):
        """
        Query tasks from table with data from **query dict
        :param query: a dict of attributes and values
        :return: query result
        """
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=%s")
            values += (v,)
        q = " AND ".join(qs)
        sql = f"SELECT * FROM passwords WHERE {q}"
        cur = self._execute_sql(sql, values)
        return cur.fetchall()

    def retrieve_password(self, name):
        """
        Query tasks from table with data from **query dict
        :param name: name to which the password is assigned
        :return: query result
        """
        sql = f"SELECT password FROM passwords WHERE name=%s"
        cur = self._execute_sql(sql, (name,))
        return cur.fetchone()

    def update(self, id, **kwargs):
        """
        update password
        :param id: row id
        :return: None
        """
        parameters = [f"{k} = %s" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id,)

        sql = f''' UPDATE passwords
                 SET {parameters}
                 WHERE id = %s'''

        try:
            self._execute_sql(sql, values)
            self.connection.commit()
        except Error as e:
            logging.error(e)

    def delete(self, table, id):
        """
        delete password
        :param table: DB table name
        :param id: row id
        :return: None
        """
        sql = f"DELETE FROM {table} WHERE id = %s"
        self._execute_sql(sql, (id,))
        self.connection.commit()
