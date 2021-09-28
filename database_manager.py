from getpass import getpass
from mysql.connector import connect, Error
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename="logfile.log")

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")


class DatabaseManager:
    def __init__(self, database):
        self.connection = self._create_connection(database)

    def _create_connection(self, database):
        """ create a database connection to a Mysql database """
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

    def __del__(self):
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


    def add_password(self, name, password):
        """
        Create a new password into the passwords table
        :param conn:
        :param password:
        :return: password id
        """
        sql = '''INSERT INTO passwords(name, password)
                 VALUES(%s, %s)'''
        cur = self._execute_sql(sql, (name, password))
        self.connection.commit()
        return cur.lastrowid


    def select_all(self):
        """
        Query all rows in the table
        :param conn: the Connection object
        :return:
        """
        sql = "SELECT * FROM passwords ORDER BY name"
        cur = self._execute_sql(sql)
        rows = cur.fetchall()
        return rows


    def select_passwords_where(self, **query):
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
        cur = self._execute_sql(sql, values)
        rows = cur.fetchall()
        return rows


    def select_password(self, name):
        """
        Query tasks from table with data from **query dict
        :param conn: the Connection object
        :param name: name to which the password is assigned
        :return:
        """
        sql = f"SELECT password FROM passwords WHERE name=%s"
        cur = self._execute_sql(sql, (name,))
        password = cur.fetchone()
        return password


    def update(self, id, **kwargs):
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
            self._execute_sql(sql, values)
            self.connection.commit()
        except Error as e:
            logging.error(e)


    def delete(self, id):
        """
        delete password
        :param conn:
        :param id: row id
        :return:
        """
        sql = "DELETE FROM passwords WHERE id=?"
        self._execute_sql(sql, (id,))
        self.connection.commit()

