import pygame
from ui.start_view import StartView
from ui.klondike_view import KlondikeView
from ui.message_view import MessageBox
from ui.clock import Clock


class UI:
    """
    Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, window_size):

        pygame.init()
        pygame.display.set_caption("Pasianssi")

        self.window_size = window_size
        self._set_window_size()

        clock = Clock()

        self.background_color = (219, 219, 200)
        self.message_box = MessageBox(self.window)
        self.start_view = StartView(self.window, self.background_color)
        self.klondike_view = KlondikeView(
            self.window, self.background_color, clock)

    def start(self):
        level = self.start_view._show()
        if level:
            self._show_klondike_view(level)

    def _show_klondike_view(self, level, start_new=True):
        won = self.klondike_view._play(start_new=start_new, level=level)
        back_to_start = self._show_message_view(won)
        if back_to_start:
            self.start()
        else:
            if not won:
                self._show_klondike_view(level, start_new=False)
            else:
                self._show_klondike_view(level, start_new=True)

    def _show_message_view(self, won):
        self.message_box._set_texts(won)
        back_to_start = self.message_box._show()
        self._set_window_size()
        return back_to_start

    def _set_window_size(self):
        self.window = pygame.display.set_mode(self.window_size)
