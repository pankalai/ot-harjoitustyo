import pygame
from ui.element import Element, Button
from ui.ui_settings import ui_settings


class MessageView:
    """Käyttäjälle näytettävien viestien näyttämisestä vastaava luokka.
    """
    texts = {
        True: {
            "question_text": "Onneksi olkoon!",
            "button2_text": "Uusi peli"
        },
        False: {
            "question_text": "Haluatko varmasti lopettaa?",
            "button2_text": "Jatka pelaamista"
        }
    }

    def __init__(self):

        self._background_color = ui_settings.background_color
        self._won = False

        width, height = ui_settings.window_size_message_view
        top_pos = height/1.5
        self._button_quit = Button("Palaa alkuun", ((
            width/2)*0.6-ui_settings.button_size_small[0]/2, top_pos), ui_settings.button_size_small, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_medium)
        self._button_continue = Button(MessageView.texts[self._won]["button2_text"], ((
            width/2)*1.4-ui_settings.button_size_small[0]/2, top_pos), ui_settings.button_size_small, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_medium)

        self._header_text = Element(
            (width/2, height/3),
            None,
            MessageView.texts[self._won]["question_text"],
            ui_settings.text_size_sub_header,
            ui_settings.text_color
        )

        self._set_texts(False)

    def _set_texts(self, won: bool):
        """Asettaa näkymän elementtien tekstit sen perusteella, onko peli mennyt läpi.

        Args:
            won (bool): True, jos peli mennyt läpi, muuten False.
        """
        if not self._won or won != self._won:
            self._header_text.set_text(MessageView.texts[won]["question_text"])
            self._button_continue.set_text(
                MessageView.texts[won]["button2_text"])
            self._won = won

    def _draw(self, window):
        """Piirtää näkymän.

        Args:
            window: Ikkuna, johon piirretään.
        """
        pygame.display.set_mode(ui_settings.window_size_message_view)

        window.fill(self._background_color)

        # Header
        self._header_text.draw(window)

        # Buttons
        self._button_quit.draw(window)
        self._button_continue.draw(window)

    def show(self, window, won: bool):
        """Vastaa näkymän näyttämisestä. Käsittelee tapahtumat.

        Args:
            window: Ikkuna, johon piirretään.
            won (bool): Onko peli mennyt läpi vai ei.

        Returns:
            True, jos käyttäjä on valinnut pelin lopettamisen, muuten False.
        """
        self._set_texts(won)
        self._draw(window)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self._button_quit.touch(event.pos):
                        return True
                    elif self._button_continue.touch(event.pos):
                        return False

                elif event.type == pygame.MOUSEMOTION:
                    if (self._button_quit.touch(event.pos)
                            or self._button_continue.touch(event.pos)):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
