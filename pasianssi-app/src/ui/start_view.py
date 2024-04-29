import pygame
from ui.element import Button, InputField


class StartView:
    """
    Pelin alkunäkymä. 
    Käyttäjänimen antaminen ja vaikeustason valinta.
    """

    button_size = (115, 60)

    button_color = (114, 214, 114)
    text_color = (16, 48, 16)
    text_color2 = (59, 19, 19)

    input_size = (175, 25)

    header_font_size = 48
    text_font_size = 24

    def __init__(self, window, background_color):
        self.window = window
        self.width, self.height = window.get_size()

        self.background_color = background_color

        self.header_font = pygame.font.Font(None, StartView.header_font_size)
        self.text_font = pygame.font.Font(None, StartView.text_font_size)

        top_pos = self.height/1.5
        self.button_easy = Button(self.window, "Helppo", ((
            self.width/2)*0.8-self.button_size[0]/2, top_pos), StartView.button_size, StartView.button_color, StartView.text_color)
        self.button_difficult = Button(self.window, "Vaikea", ((
            self.width/2)*1.2-self.button_size[0]/2, top_pos), StartView.button_size, StartView.button_color, StartView.text_color)

        self.name_field = InputField(
            self.window, (self.width/2, self.height/2), StartView.input_size)

    def _show(self):

        self.window.fill(self.background_color)

        # Header
        header = self.header_font.render(
            'Tervetuloa pelaamaan Pasianssia!', True, StartView.text_color2)
        header_rect = header.get_rect(center=(self.width/2, self.height/4))
        self.window.blit(header, header_rect)

        # Name field
        name_text = self.text_font.render(
            'Nimimerkki:', True, StartView.text_color2)
        name_text_rect = name_text.get_rect(
            center=(self.width/2-name_text.get_width()*1.5, self.height/2))
        self.window.blit(name_text, name_text_rect)
        self.name_field.draw()

        # Buttons
        self.button_easy.draw(self.window)
        self.button_difficult.draw(self.window)

        pygame.display.update()

        running = True
        level = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.button_easy.clicked(event.pos):
                        level = 1
                    elif self.button_difficult.clicked(event.pos):
                        level = 3
                    elif self.name_field.clicked(event.pos):
                        self.name_field.activate()
                    else:
                        self.name_field.passivate()

                elif event.type == pygame.MOUSEMOTION:
                    if self.name_field.rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.KEYDOWN:
                    if self.name_field.is_active():
                        if event.key == pygame.K_RETURN:
                            print(self.name_field.text)
                        elif event.key == pygame.K_BACKSPACE:
                            self.name_field.remove_char()
                        else:
                            self.name_field.add_char(event.unicode)

                if level:
                    self.window.fill(self.background_color)
                    pygame.display.update()
                    return level

            pygame.display.update()

        return None
