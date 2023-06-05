from db_manager import SQLiteManager

if __name__ == "__main__":
    movies = [
        ("Princess Mononoke", "3", "1997", "animation"),
        ("Mad Max: Fury Road", "2", "2015", "action"),
        ("Cyrano de Bergerac", "1", "1990", "comedy drama"),
    ]

    directors = [
        ("1", "Jean-Paul", "Rappeneau", "1932-04-08"),
        ("2", "George", "Miller", "1945-03-05"),
        ("3", "Hayao", "Miyazaki", "1941-01-05"),
    ]

    with SQLiteManager("sql/database.db") as db_manager:
        db_manager.create_table(
            "movies",
            ["title TEXT", "director_id TEXT", "release_date TEXT", "type TEXT"],
        )
        db_manager.create_table(
            "directors",
            ["director_id TEXT", "first_name TEXT", "last_name TEXT", "born TEXT"],
        )

        db_manager.add_values("movies", movies)
        db_manager.add_values("directors", directors)
        db_manager.display_table("movies")

        print(
            db_manager.execute_query(
                """SELECT *
                                        FROM movies NATURAL JOIN directors
                                        WHERE release_date < 2000"""
            )
        )

        db_manager.drop_table("movies")
        db_manager.drop_table("directors")
