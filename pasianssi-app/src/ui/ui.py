
from ui.start_view import StartView
from ui.klondike_view import KlondikeView
from ui.message_view import MessageView
from ui.statistics_view import StatisticsView
from repositories.game_repository import game_repository
import pygame

class UI:
    """
    Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, window):

        self.window_size = window.get_size()
        self.window = window

        self._message_view = MessageView(window)
        self._statistics_view = StatisticsView(window)
        self._start_view = StartView(window, self._statistics_view)
        self._klondike_view = KlondikeView(window)

    def start(self):
        level = self._start_view.show()
        if level:
            self._show_klondike_view(level)

    def _show_klondike_view(self, level, start_new=True):
        won = self._klondike_view._play(start_new=start_new, level=level)
        back_to_start = self._show_message_view(won)
        if back_to_start:
            self.start()
        else:
            if not won:
                self._show_klondike_view(level, start_new=False)
            else:
                self._show_klondike_view(level, start_new=True)

    def _show_message_view(self, won):
        self._message_view._set_texts(won)
        back_to_start = self._message_view._show()
        self._resize_to_original_size()
        return back_to_start

    def _resize_to_original_size(self):
        self.window = pygame.display.set_mode(self.window_size)
