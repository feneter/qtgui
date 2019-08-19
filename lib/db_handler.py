import sqlite3
from lib.utils import db_location


class DBHandler():

    def __init__(self, db_name=""):
        self.__db_name = db_name
        self.__connection = sqlite3.connect(f"{db_location}/{self.__db_name}")
        # self.__connection = sqlite3.connect(":memory:")
        self.create_table()

    @property
    def __cursor(self):
        """
        Returns the cursor for the handler.
        """
        return self.__connection.cursor()

    def insert(self, table, **values):
        """
        Inserts one row of data into the database
        """
        print(f"Saving data to table: {table}")
        # keys, values = self.__get_key_value_placeholders(values)
        # placeholder = ",".join(["?" for _ in values])
        # print(f'"INSERT INTO {table} VALUES {placeholder}", {values}')
        # self.__cursor.execute(f"INSERT INTO {table} VALUES ({placeholder})", values)
        # self.__connection.commit()

    def insert_many(self, table, **values):
        """
        Inserts multiple rows of data into the database
        """
        if len(values) < 1:
            # TODO: raise exception here instead of just returning
            return 
        if len(values) == 1:
            self.insert(values[0])
            return
        placeholder = ",".join(["?" for _ in values[0]])
        print(f"INSERT INTO {table} VALUES {placeholder} {values}")
        self.__cursor.executemany(f"INSERT INTO {table} VALUES ({placeholder})", values)
        self.__connection.commit()

    def fetch(self, table):
        return [row for row in self.__cursor.execute(f"SELECT * FROM {table}")]

    def fetch_one(self, table, **where):
        """
        Returns one record from the database
        """
        self.__fetch(table, where)
        return self.__cursor.fetchone()

    def fetch_many(self, table, **where):
        """
        Returns a list of all records that match the search criteria given
        """
        self.__fetch(table, where)
        return self.__cursor.fetchall()

    def __fetch(self, table, **kwargs):
        if not kwargs:
            self.__cursor.execute(f"SELECT * FROM {table}")
            return
        key_placeholder, values = self.__get_key_value_placeholders(kwargs)
        self.__cursor.execute(f"SELECT * FROM {table} WHERE {key_placeholder}", values)

    def create_table(self):
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS backup_config (filename text)")

    def delete(self, table, **where):
        keys, values = self.__get_key_value_placeholders(where)
        print(f'"DELETE FROM {table} WHERE {keys}", {values}')
        # self.__cursor.execute(f"DELETE FROM {table} WHERE {keys}", values)
    
    def __get_key_value_placeholders(self, kwargs):
        key_placeholder = ""
        values = []
        for key, value in kwargs.items():
            key_placeholder += f"{key}=?,"
            values.append(value)
        return key_placeholder[:-1], tuple(values)