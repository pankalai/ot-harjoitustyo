from ui.start_view import StartView
from ui.klondike_view import KlondikeView


class UI:
    """
    Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, window):
        self.window = window

    def start(self):
        game = StartView(self.window)
        level = game._start()
        if level:
            self._show_klondike_view(level)

    def _show_klondike_view(self, level):
        klondike = KlondikeView(self.window, level)
        klondike._start()
        self.start()