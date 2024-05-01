from database_connection import get_database_connection


class GameRepository:

    def __init__(self, connection):
        self.__connection = connection
        self.cursor = self.__connection.cursor()

    def find_all_plays(self):
        self.cursor.execute("SELECT * FROM plays")
        rows = self.cursor.fetchall()
        return list(rows)
    
    def find_top_plays_by_moves(self, game, level):
        self.cursor.execute("""
            SELECT p.username,p.moves FROM plays as p
            JOIN games_and_levels gal ON gal.id = p.games_and_levels_id
            JOIN games as g ON g.id = gal.game_id
            WHERE g.name = ? and gal.level = ? and p.success = True
            ORDER BY moves
            LIMIT 5
        """, [game,level])
        rows = self.cursor.fetchall()
        return list(rows)
    
    def find_top_plays_by_time(self, game, level):
        self.cursor.execute("""
            SELECT p.username,p.start_time,p.end_time FROM plays as p
            JOIN games_and_levels gal ON gal.id = p.games_and_levels_id
            JOIN games as g ON g.id = gal.game_id
            WHERE g.name = ? and gal.level = ? and p.success = True
            ORDER BY ROUND((JULIANDAY(end_time) - JULIANDAY(start_time)) * 86400)
            LIMIT 5
        """, [game,level])
        rows = self.cursor.fetchall()
        return list(rows)

    def add(self, username, start_time, end_time, moves, success, game, level):
        games_and_levels_id = ""

        self.cursor.execute(
            """"
            insert into users (username, start_time, end_time, moves, success, games_and_levels_id) 
            values (?, ?, ?, ?, ?)
            """,
            (username, start_time, end_time, moves, success, games_and_levels_id)
        )

        self._connection.commit()


game_repository = GameRepository(get_database_connection())
