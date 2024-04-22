from ui.start_view import StartView
from ui.klondike_view import KlondikeView


class UI:
    """
    Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, window):
        self.window = window
        self.background_color = (219,219,200)

    def start(self):
        game = StartView(self.window, self.background_color)
        level = game._start()
        if level:
            self._show_klondike_view(level)

    def _show_klondike_view(self, level):
        klondike = KlondikeView(self.window, self.background_color, level)
        won = klondike._play()
        # if won:
        #     if self._show_message_view(won):
        #         self._show_klondike_view(level)
        self.start()
