from services.clock import get_current_time
from repositories.game_repository import game_repository


class GameService:
    """Pelin käynnistämisestä ja tallentamisesta vastaava luokka.
    """

    def __init__(self, game, player: str, game_loop, repository=game_repository):
        """Luokan konstruktori.

        Args:
            game: Pelin logiikasta vastaava olio.
            player (str): Pelaajan nimi.
            game_loop: Pelisilmukasta vastaava olio.
            repository: Pelin tietojen tallentamisesta vastaava olio.
        """
        self.id = game_repository.get_next_id()
        self.player_name = player if player else "anonyymi" + str(self.id)

        self._game = game
        self._repository = repository
        self._game_loop = game_loop

        self._save()

    def play(self, new_game=True):
        """Käynnistää pelisilmukan.

        Args:
            new_game (bool, optional): Aloitetaanko kokonaan uusi peli.
        """
        self._game_loop.start(new_game)
        self._save()

    def _save(self):
        """Tallentaa pelin tiedot.
        """
        self._repository.add_played_game(self)

    @property
    def game_name(self):
        """Palauttaa pelin nimen.

        Returns:
           Nimi merkkijonona.
        """
        return self._game.name

    @property
    def game_level(self):
        """Palauttaa pelin tason

        Returns:
           Taso kokonaislukuna.
        """
        return self._game.level

    @property
    def game_won(self):
        """Palauttaa tiedon, onko peli mennyt läpi.

        Returns:
           True, jos peli on mennyt läpi, muuten False.
        """
        return self._game.game_won()

    @property
    def moves(self):
        """Palauttaa pelissä tehtyjen siirtojen määrän.

        Returns:
            Siirtojen määrä.
        """
        return self._game_loop.get_moves()

    @property
    def start_time(self):
        """Palauttaa ajan, jolloin peli aloitettiin.

        Returns:
            Alkamisaika.
        """
        return self._game_loop.get_start_time()

    @property
    def end_time(self):
        """Palauttaa pelin päättymisajan.

        Returns:
           Tämänhetkinen aika.
        """
        return get_current_time()
