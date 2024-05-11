import pygame
from repositories.game_repository import game_repository
from ui.element import Element, Button
from ui.ui_settings import ui_settings
from services.clock import time_diff_in_hours_minutes_seconds, string_to_datetime


class StatisticsView:
    """Pelattujen pelien tilastojen näyttämisestä vastaava luokka.
    """

    def __init__(self):
        self.background_color = ui_settings.background_color

        self._header_text = Element(
            None,
            None,
            "Parhaat tulokset",
            ui_settings.text_size_header,
            ui_settings.text_color
        )

        # Sarake 1 (helpot)
        self._header1 = Element(None, None, "HELPPO",
                                ui_settings.text_size_sub_header, ui_settings.text_color)
        self._sub_header1_1 = Element(
            None, None, "Aika", ui_settings.text_size_medium, ui_settings.text_color)
        self._sub_header1_1.set_underline()
        self._sub_header1_2 = Element(
            None, None, "Siirrot", ui_settings.text_size_medium, ui_settings.text_color)
        self._sub_header1_2.set_underline()

        # Sarake 2 (vaikeat)
        self._header2 = Element(None, None, "VAIKEA",
                                ui_settings.text_size_sub_header, ui_settings.text_color)
        self._sub_header2_1 = Element(
            None, None, "Aika", ui_settings.text_size_medium, ui_settings.text_color)
        self._sub_header2_1.set_underline()
        self._sub_header2_2 = Element(
            None, None, "Siirrot", ui_settings.text_size_medium, ui_settings.text_color)
        self._sub_header2_2.set_underline()

        self._sub_headers = [self._header1, self._sub_header1_1, self._sub_header1_2,
                             self._header2, self._sub_header2_1, self._sub_header2_2]

        self._button_back = Button("Takaisin", None, ui_settings.button_size_big,
                                   ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_big)

    def _set_positions(self, window):
        """Asettaa näkymän elementtien sijainnit.

        Args:
            window : Ikkuna, johon elementit piirretään.
        """
        width, height = window.get_size()
        self._header_text.set_position((width/2, 50))

        start_pos1 = width/7.5, height/4.5
        self._header1.set_position(start_pos1)
        self._sub_header1_1.set_position(row_offset(start_pos1, (125, 15)))
        self._sub_header1_2.set_position(row_offset(start_pos1, (325, 15)))

        start_pos2 = width/7.5, height/1.85
        self._header2.set_position(start_pos2)
        self._sub_header2_1.set_position(row_offset(start_pos2, (125, 15)))
        self._sub_header2_2.set_position(row_offset(start_pos2, (325, 15)))

        self._button_back.set_position(
            (width/2-ui_settings.button_size_big[0]/2,
             height-ui_settings.button_size_big[1]*1.25)
        )

    def _get_data(self):
        """Hakee datan.
        """
        self.top_by_time1 = game_repository.get_top_played_games_by_time(
            "Klondike", 1)
        self.top_by_moves1 = game_repository.get_top_played_games_by_moves(
            "Klondike", 1)
        self.top_by_time3 = game_repository.get_top_played_games_by_time(
            "Klondike", 3)
        self.top_by_moves3 = game_repository.get_top_played_games_by_moves(
            "Klondike", 3)

    def _draw_table(self, window):
        """Piirtää tilastodatan taulukkoon

        Args:
            window: Ikkuna, johon piirretään.
        """
        offset = 20, 90

        # By time
        lists = [self.top_by_time1, self.top_by_time3]
        for i, header in enumerate([self._sub_header1_1, self._sub_header2_1]):
            left, top = row_offset(header.get_position(), (0, 25))
            for row in lists[i]:
                elem1 = Element(
                    (left, top), None, row["username"], ui_settings.text_size_medium, ui_settings.text_color)
                elem1.draw(window)
                elem2 = Element((left+offset[1], top), None, time_diff_in_hours_minutes_seconds(string_to_datetime(
                    row["start_time"]), string_to_datetime(row["end_time"])), ui_settings.text_size_medium, ui_settings.text_color)
                elem2.draw(window)
                top += offset[0]

        # By moves
        lists = [self.top_by_moves1, self.top_by_moves3]
        for i, header in enumerate([self._sub_header1_2, self._sub_header2_2]):
            left, top = row_offset(header.get_position(), (0, 25))
            for row in lists[i]:
                elem1 = Element(
                    (left, top), None, row["username"], ui_settings.text_size_medium, ui_settings.text_color)
                elem1.draw(window)
                elem2 = Element((left+offset[1], top), None, str(row["moves"]),
                                ui_settings.text_size_medium, ui_settings.text_color)
                elem2.draw(window)
                top += offset[0]

    def _draw(self, window):
        """Piirtää näkymän.

        Args:
            window: Ikkuna, johon piirretään.
        """
        window.fill(self.background_color)

        # Headers
        self._header_text.draw(window)

        for header in self._sub_headers:
            header.draw(window)

        # Tables
        self._draw_table(window)

        # Button
        self._button_back.draw(window)

    def show(self, window):
        """Vastaa näkymän näyttämisestä. Käsittelee tapahtumat.

        Args:
            window: Ikkuna, johon piirretään.
        """
        self._get_data()
        self._set_positions(window)

        self._draw(window)

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self._button_back.touch(event.pos):
                        running = False

                elif event.type == pygame.MOUSEMOTION:
                    if self._button_back.touch(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def row_offset(start, offset):
    return start[0]+offset[0], start[1]+offset[1]
