import sqlite3
from typing import Callable, Concatenate, Iterable, ParamSpec, Self, TypeVar
from functools import wraps

T = TypeVar("T")
P = ParamSpec("P")


class SQLiteManager:
    def __init__(self, db_path: str) -> None:
        """Create a SQLiteManager

        Args:
            path (str): path to the database
        """
        print("INIT")
        self.db_path = db_path
        self.conn: None | sqlite3.Connection = None
        self.cursor: None | sqlite3.Cursor = None

    def connect(self) -> None:
        """Establish a connection to a db"""

        if self.conn is None:
            print("CONNECT")
            self.conn = sqlite3.connect(self.db_path)
        if self.cursor is None:
            self.cursor = self.conn.cursor()

    def check_connection(
        func: Callable[Concatenate[Self, P], T]
    ) -> Callable[Concatenate[Self, P], T]:
        @wraps(func)
        def wrapper(self: Self, *args: P.args, **kwargs: P.kwargs) -> T:
            self.connect()
            return func(self, *args, **kwargs)

        return wrapper

    @check_connection
    def create_table(self, table_name: str, columns: Iterable[str]) -> None:
        query = f"""CREATE TABLE {table_name} ({", ".join(columns)});"""
        print(query)
        self.cursor.execute(query)
        self.conn.commit()

    @check_connection
    def drop_table(self, table_name: str, if_exists=True) -> None:
        if_exists_text = "IF EXISTS" if if_exists else ""
        query = f"""DROP TABLE {if_exists_text} {table_name}"""
        print(query)
        self.cursor.execute(query)
        self.conn.commit()

    @check_connection
    def add_values(self, table_name: str, values: Iterable[Iterable[str]]) -> None:
        query = f"""INSERT INTO {table_name}
                    VALUES ({",".join("?" for i in range(len(values[0])))})"""
        print(query)
        self.cursor.executemany(query, values)
        self.conn.commit()

    @check_connection
    def display_table(self, table_name: str) -> None:
        query = f"""SELECT * FROM {table_name}"""
        print(query)
        self.cursor.execute(query)
        print(self.cursor.fetchall())

    @check_connection
    def execute_query(self, query: str) -> Iterable[Iterable[str]] | Iterable[str]:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        """
        Close a connection
        """
        if self.conn is not None:
            print("CLOSE")
            self.conn.close()
            self.conn = None
        if self.cursor is not None:
            self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
