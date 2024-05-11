from database_connection import get_database_connection


class GameRepository:
    """Pelattuihin pelehin liittyvistä tietokantaoperaatioista vastaava luokka.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Tietokantayhteyden Connection-olio.
        """
        self._connection = connection
        self._cursor = self._connection.cursor()

    def get_next_id(self):
        """Palauttaa played_games taulun seuraavan id:n.

        Returns:
            1 jos pelattujen pelien taulu on tyhjä, 
            muuten yhden isomman kuin on suurin id.
        """
        self._cursor.execute("SELECT max(id) FROM played_games")
        played_games_id = self._cursor.fetchone()[0]
        return 1 if not played_games_id else played_games_id+1

    def delete_all_played_games(self):
        """Poistaa kaikki pelatut pelit.
        """
        self._cursor.execute("DELETE FROM played_games")
        self._connection.commit()

    def delete_all_games(self):
        """Poistaa kaikki pelit.
        """
        self._cursor.execute("DELETE FROM games")
        self._connection.commit()

    def delete_all_games_and_levels(self):
        """Poistaa kaikki tasot.
        """
        self._cursor.execute("DELETE FROM games_and_levels")
        self._connection.commit()

    def get_all_played_games(self):
        """Palauttaa kaikki pelatut pelit.

        Returns:
            Lista rivejä.
        """
        self._cursor.execute("SELECT * FROM played_games")
        rows = self._cursor.fetchall()
        return rows

    def _find_by_id(self, game_id: int):
        """Palauttaa tiedon löytyykö pelin id tietokannasta.

        Args:
            game_id (int): Haettavan pelin id.

        Returns:
            True jos id löytyy, muuten False
        """
        self._cursor.execute(
            "SELECT * FROM played_games WHERE id = ?", (game_id,))
        row = self._cursor.fetchone()
        return row

    def find_by_game_name(self, name: str):
        """Hakee pelin nimen perusteella.

        Args:
            name (str): Pelin nimi.

        Returns:
            Pelin id, jos peli löytyy tietokannasta, muuten None.
        """
        self._cursor.execute(
            "SELECT * FROM games WHERE name = ?", (name,))
        row = self._cursor.fetchone()
        return row["id"] if row else None

    def add_game(self, name: str):
        """Lisää pelin tietokantaan.

        Args:
            name (str): Pelin nimi.
        Returns:
            Lisätyn pelin id.
        """
        self._cursor.execute(
            "INSERT INTO games (name) VALUES (?)", (name,))
        self._connection.commit()
        return self._cursor.lastrowid

    def find_by_game_level(self, game_id: int, level: int):
        """Hakee peliä ja tasoa

        Args:
            game_id (int): Pelin id.
            level (int): Pelin taso.

        Returns:
            Pelin ja tason id, jos ne löytyvät tietokannasta, muuten None.
        """
        self._cursor.execute(
            "SELECT * FROM games_and_levels WHERE game_id = ? and level = ?", (game_id, level,))
        row = self._cursor.fetchone()
        return row["id"] if row else None

    def add_game_level(self, level: int, game_id: int):
        """Lisää pelille uuden tason.

        Args:
            level (int): Pelin taso.
            game_id (int): Pelin id.

        Returns:
            Lisätyn pelin ja tason id.
        """
        self._cursor.execute(
            "INSERT INTO games_and_levels (level, game_id) VALUES (?, ?)", (level, game_id))
        self._connection.commit()
        return self._cursor.lastrowid

    def get_top_played_games_by_moves(self, game: str, level: int):
        """Palauttaa parhaat tulokset siirtomäärän mukaan.

        Args:
            game (str): Pelin nimi.
            level (int): Pelin taso.

        Returns:
            Tietokannan rivit listana.
        """
        self._cursor.execute("""
            SELECT p.username,p.moves FROM played_games as p
            JOIN games_and_levels gal ON gal.id = p.games_and_levels_id
            JOIN games as g ON g.id = gal.game_id
            WHERE g.name = ? and gal.level = ? and p.success = True
            ORDER BY moves
            LIMIT 5
        """, [game, level])
        rows = self._cursor.fetchall()
        return list(rows)

    def get_top_played_games_by_time(self, game: str, level: int):
        """Palauttaa parhaat tulokset käytetyn ajan mukaan.

        Args:
            game (str): Pelin nimi.
            level (int): Pelin taso.

        Returns:
            Tietokannan rivit listana.
        """
        self._cursor.execute("""
            SELECT p.username,p.start_time,p.end_time FROM played_games as p
            JOIN games_and_levels gal ON gal.id = p.games_and_levels_id
            JOIN games as g ON g.id = gal.game_id
            WHERE g.name = ? and gal.level = ? and p.success = True
            ORDER BY ROUND((JULIANDAY(end_time) - JULIANDAY(start_time)) * 86400)
            LIMIT 5
        """, [game, level])
        rows = self._cursor.fetchall()
        return list(rows)

    def add_played_game(self, played_game):
        """Tallentaa pelin tiedot tietokantaan. 
        Lisää pelin ja tason tietokantaan, jos niitä ei vielä ole.

        Args:
            game (GameService): GameService-luokan olio, jonka tietoja lisätään tietokantaan.
        """
        if self._find_by_id(played_game.id):
            self.update_played_game(played_game)
        else:
            game_id = self.find_by_game_name(played_game.game_name)
            if not game_id:
                new_game_id = self.add_game(played_game.game_name)
                self.add_game_level(played_game.game_level, new_game_id)
            elif not self.find_by_game_level(game_id, played_game.game_level):
                self.add_game_level(played_game.game_level, game_id)

            self.insert_played_game(played_game)

    def insert_played_game(self, played_game):
        """Lisää uuden pelin tiedot tietokantaan.
        """
        self._cursor.execute(
            """
            INSERT INTO played_games (id, username, start_time, end_time,
            moves, success, games_and_levels_id) 
            SELECT ?, ?, ?, ?, ?, ?, gal.id
            FROM games as g
            JOIN games_and_levels as gal on gal.game_id = g.id
            WHERE g.name = ? and gal.level = ?
            """,
            (played_game.id, played_game.player_name, played_game.start_time, played_game.end_time,
             played_game.moves, played_game.game_won, played_game.game_name, played_game.game_level)
        )

        self._connection.commit()

    def update_played_game(self, played_game):
        """Päivittää pelin tiedot tietokantaan.
        """
        self._cursor.execute(
            """
            update played_games 
            set start_time = ?, end_time = ?, moves = ?, success = ?
            where id = ?
            """,
            (played_game.start_time, played_game.end_time,
             played_game.moves, played_game.game_won, played_game.id)
        )

        self._connection.commit()


game_repository = GameRepository(get_database_connection())
