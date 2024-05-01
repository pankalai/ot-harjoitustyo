import pygame
from ui.element import Element, Button, InputField
import ui_settings

class StartView:
    """
    Pelin alkunäkymä. 
    Käyttäjänimen antaminen ja vaikeustason valinta.
    """

    def __init__(self, window, statistics_view):
        self.window = window
        self.width, self.height = window.get_size()

        self.background_color = ui_settings.background_color
        self._statistics_view = statistics_view

        self.header_text = Element(
            self.window,
            (self.width/2, self.height/4),
            None,
            "Tervetuloa pelaamaan Pasianssia!",
            ui_settings.text_size_header,
            ui_settings.text_color
        )

        self.name_field = InputField(
            self.window, (self.width/2, self.height/2.25), ui_settings.input_size)
        
        self.name_text = Element(
            self.window,
            (self.width/2-150, self.height/2.25),
            None,
            "Nimimerkki:",
            ui_settings.text_size_big,
            ui_settings.text_color
        )

        self.statistics_text = Element(
            self.window,
            (self.width/2, self.height/1.75),
            None,
            "Katso tilastoja",
            ui_settings.text_size_big,
            ui_settings.link_color
        )

        top_pos = self.height/1.4
        self.button_easy = Button(self.window, "Helppo", ((
            self.width/2)*0.8-ui_settings.button_size_big[0]/2, top_pos), ui_settings.button_size_big, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_big)
        self.button_difficult = Button(self.window, "Vaikea", ((
            self.width/2)*1.2-ui_settings.button_size_big[0]/2, top_pos), ui_settings.button_size_big, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_big)

    def init_view(self):
        self.window.fill(self.background_color)

        # Header
        self.header_text.draw()

        # Name field
        self.name_text.draw()
        self.name_field.passivate()
        self.name_field.draw()

        # Statistics text
        self.statistics_text.set_underline()
        self.statistics_text.draw()

        # Buttons
        self.button_easy.draw()
        self.button_difficult.draw()

    def show(self):
        
        self.init_view()
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.button_easy.touch(event.pos):
                        return 1
                    elif self.button_difficult.touch(event.pos):
                        return 3
                    elif self.name_field.touch(event.pos):
                        self.name_field.activate()
                    elif self.statistics_text.touch(event.pos):
                        self._statistics_view.show()
                        self.init_view()
                    else:
                        self.name_field.passivate()

                elif event.type == pygame.KEYDOWN:
                    if self.name_field.is_active():
                        if event.key == pygame.K_RETURN:
                            self.name_field.passivate()
                        elif event.key == pygame.K_BACKSPACE:
                            self.name_field.remove_char()
                        else:
                            self.name_field.add_char(event.unicode)

                elif event.type == pygame.MOUSEMOTION:
                    if self.name_field.touch(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                    elif (self.statistics_text.touch(event.pos)
                            or self.button_easy.touch(event.pos)
                            or self.button_difficult.touch(event.pos)):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()

            