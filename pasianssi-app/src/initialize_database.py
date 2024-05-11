from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists games;
    """)
    cursor.execute("""
        drop table if exists games_and_levels;
    """)
    cursor.execute("""
        drop table if exists played_games;
    """)

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        create table games (
            id INTEGER PRIMARY KEY,
            name TEXT 
        );
    """)

    cursor.execute("""
        create table games_and_levels (
            id INTEGER PRIMARY KEY,
            level INTEGER,
            game_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES games(id)
        );
    """)

    cursor.execute("""
        create table played_games (
            id INTEGER PRIMARY KEY,
            username TEXT,
            start_time DATETIME,
            end_time DATETIME,
            moves INTEGER,
            success BOOLEAN,
            games_and_levels_id INTEGER,
            FOREIGN KEY (games_and_levels_id) REFERENCES games_and_levels(id)       
        );
    """)

    connection.commit()


def insert_data(connection):
    cursor = connection.cursor()

    # Games
    cursor.execute("""
        INSERT INTO games (name) VALUES ("Klondike");
    """)

    # Games and levels
    cursor.execute("""
        INSERT INTO games_and_levels (level,game_id) VALUES (1,1);
    """)
    cursor.execute("""
        INSERT INTO games_and_levels (level,game_id) VALUES (3,1);
    """)

    # played_games
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("matti","2024-04-26 12:01:22","2024-04-26 12:31:52",67,True,1);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("liisa","2024-04-26 12:02:22","2024-04-26 12:32:08",74,True,1);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("mari","2024-04-26 12:02:22","2024-04-26 12:09:43",79,True,1);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("antti","2024-04-26 12:02:22","2024-04-26 12:15:03",109,True,1);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("jussi","2024-04-26 12:02:22","2024-04-26 12:06:18",54,True,1);
    """)
    ######
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("tero","2024-04-26 12:02:22","2024-04-26 12:13:25",89,True,2);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("anu","2024-04-26 12:02:22","2024-04-26 12:21:19",105,True,2);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("minna","2024-04-26 12:02:22","2024-04-26 12:41:37",71,True,2);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("jani","2024-04-26 12:02:22","2024-04-26 12:22:07",94,True,2);
    """)
    cursor.execute("""
        INSERT INTO played_games (username,start_time,end_time,moves,success,games_and_levels_id) 
        VALUES ("pekka","2024-04-26 12:02:22","2024-04-26 12:55:17",77,True,2);
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)
    insert_data(connection)


if __name__ == "__main__":
    initialize_database()
