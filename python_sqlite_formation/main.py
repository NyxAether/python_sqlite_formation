import os
from db_manager import SQLiteManager


with SQLiteManager("sql/database.db") as db_manager:

    db_manager.create_table(
        "books", ["title TEXT", "author TEXT", "release_date TEXT", "book_type TEXT"]
    )

    db_manager.drop_table("books")


# db_manager = SQLiteManager("../sql/database.db")
# db_manager.create_table(
#     "books", ["title TEXT", "author TEXT", "release_date TEXT", "book_type TEXT"]
# )
