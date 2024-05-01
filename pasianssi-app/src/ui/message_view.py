import pygame
from ui.element import Element, Button
import ui_settings


class MessageView:

    def __init__(self, window, won=False):

        self.window = window
        self.background_color = ui_settings.background_color
        self.width, self.height = ui_settings.window_size_message_view

        self.texts = {
            True: {
                "question_text": "Onneksi olkoon!",
                "button2_text": "Uusi peli"
            },
            False: {
                "question_text": "Haluatko varmasti lopettaa?",
                "button2_text": "Jatka pelaamista"
            }
        }

        top_pos = self.height/1.5
        self.button_quit = Button(self.window, "Palaa alkuun", ((
            self.width/2)*0.6-ui_settings.button_size_small[0]/2, top_pos), ui_settings.button_size_small, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_medium)
        self.button_continue = Button(self.window, self.texts[won]["button2_text"], ((
            self.width/2)*1.4-ui_settings.button_size_small[0]/2, top_pos), ui_settings.button_size_small, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_medium)

        self.header_text = Element(
            self.window,
            (self.width/2, self.height/3),
            None,
            self.texts[won]["question_text"],
            ui_settings.text_size_sub_header,
            ui_settings.text_color
        )

        self.won = won
        self._set_texts(won)

    def _set_texts(self, won):
        if not self.won or won != self.won:
            self.header_text.set_text(self.texts[won]["question_text"])
            self.button_continue.set_text(self.texts[won]["button2_text"])
            self.won = won

    def _show(self):
        pygame.display.set_mode(ui_settings.window_size_message_view)
        
        self.window.fill(self.background_color)

        # Header
        self.header_text.draw()

        # Buttons
        self.button_quit.draw()
        self.button_continue.draw()

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.button_quit.touch(event.pos):
                        return True
                    elif self.button_continue.touch(event.pos):
                        return False
                
                elif event.type == pygame.MOUSEMOTION:
                    if (self.button_quit.touch(event.pos)
                            or self.button_continue.touch(event.pos)):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)                
