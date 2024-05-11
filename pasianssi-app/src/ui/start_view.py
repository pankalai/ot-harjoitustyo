import pygame
from ui.element import Element, Button, InputField
from ui.ui_settings import ui_settings
from ui.statistics_view import StatisticsView
from services.klondike import klondike_service


class StartView:
    """
    Pelin alkunäkymä. 
    Käyttäjänimen antaminen ja vaikeustason valinta.
    """

    def __init__(self):
        self._background_color = ui_settings.background_color
        self._statistics_view = StatisticsView()

        self._game = klondike_service

        self._header_text = Element(
            None,
            None,
            "Tervetuloa pelaamaan Pasianssia!",
            ui_settings.text_size_header,
            ui_settings.text_color
        )

        self._name_field = InputField(
            None, ui_settings.input_size)

        self._name_text = Element(
            None,
            None,
            "Nimimerkki:",
            ui_settings.text_size_big,
            ui_settings.text_color
        )

        self._statistics_text = Element(
            None,
            None,
            "Katso tilastoja",
            ui_settings.text_size_big,
            ui_settings.link_color
        )

        self._button_easy = Button(
            "Helppo",
            None,
            ui_settings.button_size_big,
            ui_settings.button_color,
            ui_settings.link_color,
            ui_settings.text_size_big,
        )

        self._button_difficult = Button(
            "Vaikea",
            None,
            ui_settings.button_size_big,
            ui_settings.button_color,
            ui_settings.link_color,
            ui_settings.text_size_big,
        )

    def get_player_name(self):
        return self._name_field.get_text().strip()

    def _set_positions(self, window):
        width, height = window.get_size()
        self._header_text.set_position((width/2, height/4))
        self._name_field.set_position((width/2, height/2.25))
        self._name_text.set_position(
            (width/2-self._name_field.get_size()[0]*0.85, height/2.25+3))
        self._statistics_text.set_position((width/2, height/1.75))

        top_pos = height/1.4
        self._button_easy.set_position(
            ((width/2)*0.8-ui_settings.button_size_big[0]/2, top_pos))
        self._button_difficult.set_position(
            ((width/2)*1.2-ui_settings.button_size_big[0]/2, top_pos))

    def _draw(self, window):
        window.fill(self._background_color)

        self._header_text.draw(window)

        self._name_text.draw(window)
        self._name_field.passivate(window)
        self._name_field.draw(window)

        self._statistics_text.set_underline()
        self._statistics_text.draw(window)

        self._button_easy.draw(window)
        self._button_difficult.draw(window)

    def show(self, window):
        """Vastaa näkymän näyttämisestä. Käsittelee tapahtumat.

        Args:
            window: Ikkuna, johon piirretään.

        Returns:
            Palauttaa pelin, jos käyttäjä niin valitsee.
        """
        self._set_positions(window)
        self._draw(window)

        running = True
        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._button_easy.touch(event.pos):
                        self._game.set_level(1)
                        return self._game
                    elif self._button_difficult.touch(event.pos):
                        self._game.set_level(3)
                        return self._game
                    elif self._name_field.touch(event.pos):
                        self._name_field.activate(window)
                    elif self._statistics_text.touch(event.pos):
                        self._statistics_view.show(window)
                        self._draw(window)
                    else:
                        self._name_field.passivate(window)

                elif event.type == pygame.KEYDOWN:
                    if self._name_field.is_active():
                        if event.key == pygame.K_RETURN:
                            self._name_field.passivate(window)
                        elif event.key == pygame.K_BACKSPACE:
                            self._name_field.remove_char(window)
                        else:
                            self._name_field.add_char(
                                event.unicode, window)

                elif event.type == pygame.MOUSEMOTION:
                    if self._name_field.touch(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                    elif (self._statistics_text.touch(event.pos)
                            or self._button_easy.touch(event.pos)
                            or self._button_difficult.touch(event.pos)):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()
