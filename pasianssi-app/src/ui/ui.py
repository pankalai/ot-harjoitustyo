
from ui.start_view import StartView
from ui.message_view import MessageView
from ui.ui_settings import ui_settings
from services.game_service import GameService
from services.game_loop import GameLoop
from services.renderer import GameRenderer
import pygame


class UI:
    """
    Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, window):
        self._window = window

        self._message_view = MessageView()
        self._start_view = StartView()

        self._game_service = None

    def show(self):
        """Näyttää alkunäkymän
        """
        game = self._start_view.show(self._window)
        if game:
            self._start_game(game)

    def _start_game(self, game, start_new=True):
        """Käynnistää pelin.

        Args:
            game: Peli, joka käynnistetään.
            start_new (bool, optional): Aloitetaanko kokonaan uusi peli vai jatketaan jo aloitettua.
        """
        if start_new or not self._game_service:
            self._game_service = GameService(
                game,
                self._start_view.get_player_name(),
                GameLoop(game, GameRenderer(self._window))
            )
        self._game_service.play(start_new)
        won = self._game_service.game_won
        back_to_start = self._show_message_view(won)
        if back_to_start:
            self.show()
        else:
            if not won:
                self._start_game(game, start_new=False)
            else:
                self._start_game(game, start_new=True)

    def _show_message_view(self, won: bool):
        """Näyttää viestinäkymän.

        Args:
            won (bool): Onko peli mennyt läpi vai ei.

        Returns:
            True, jos palataan alkuun, muuten False.
        """
        back_to_start = self._message_view.show(self._window, won)
        self._resize_to_original_size()
        return back_to_start

    def _resize_to_original_size(self):
        """Asettaa ikkunan koon alkuperäiseksi.
        """
        self._window = pygame.display.set_mode(ui_settings.window_size)
