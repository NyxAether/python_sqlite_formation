import sqlite3

if __name__ == "__main__":
    movies = [
        ("Princess Mononoke", "3", "1997", "animation"),
        ("Mad Max: Fury Road", "2", "2015", "action"),
        ("Cyrano de Bergerac", "1", "1990", "comedy drama"),
    ]

    # Open a connection
    connection = sqlite3.connect("sql/database.db")
    cursor = connection.cursor()

    # Create tables in a dataset
    query = f"""CREATE TABLE movies ({", ".join(["title TEXT", "director_id TEXT", "release_date TEXT", "type TEXT"])});"""
    cursor.execute(query)
    # Insert values
    query = f"""INSERT INTO movies VALUES ({",".join("?" for i in range(len(movies[0])))})"""
    for movie in movies:
        cursor.execute(query, movie)
    # Commit the database modifications
    connection.commit()

    # # Drop table
    # query = """DROP TABLE movies"""
    # cursor.execute(query)
    # connection.commit()

    connection.close()
    # # Since connection is closed, a sqlite.ProgrammingError will occur
    # query = """SELECT * FROM movies"""
    # cursor.execute(query)
