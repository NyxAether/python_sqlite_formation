from contextlib import contextmanager
import sqlite3
from typing import Any, Callable, Iterable, TypeVar
from functools import wraps


class SQLiteManager:
    def __init__(self, db_path: str) -> None:
        """Create a SQLiteManager

        Args:
            path (str): path to the database
        """
        print("INIT")
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a connection to a db
        """
        
        if self.conn is None:
            print("CONNECT")
            self.conn = sqlite3.connect(self.db_path)
        if self.cursor is None:
            self.cursor = self.conn.cursor()

    def check_connection(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            args[0].connect()
            return func(*args, **kwargs)

        return wrapper

    @check_connection
    def create_table(self, table_name: str, columns: Iterable[str]) -> None:
        query = f"""CREATE TABLE {table_name} ({", ".join(columns)});"""
        print(query)
        self.cursor.execute(query)
        self.conn.commit()

    @check_connection
    def drop_table(self, table_name: str, if_exists=True):
        if_exists_text = "IF EXISTS" if if_exists else ""
        query =f"""DROP TABLE {if_exists_text} {table_name}"""
        print(query)
        self.cursor.execute(query)
        self.conn.commit()

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
