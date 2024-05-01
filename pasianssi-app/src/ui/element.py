import pygame


class Element:
    text_color = (5, 5, 5)

    background_color = (219, 219, 219)
    text_size = 22
    border_size = 1

    def __init__(self, window, position = None, size = None, text = "", text_size = None, text_color = None) -> None:
        self.window = window
        self.position = position

        self.text = text
        self.text_color = text_color if text_color else Element.text_color
        self.text_size = text_size if text_size else Element.text_size

        self.font = pygame.font.Font(None, self.text_size)
        self.text_font = self.font.render(self.text, True, self.text_color)
        
        self.size = size if size else (self.text_font.get_rect().width,self.text_font.get_rect().height) 

        self.field = pygame.Surface(self.size).convert()
        self.rect = self.field.get_rect(
            center=(self.position[0], self.position[1]))

    def draw(self):
        self.window.blit(self.text_font, self.rect)

    def set_text(self, text):
        self.text_font = self.font.render(text, True, self.text_color)

    def set_underline(self):
        self.font.set_underline(True)
        self.text_font = self.font.render(
            self.text, True, self.text_color)

    def get_position(self):
        return self.position
    
    def draw_border(self):
        border_size = Element.border_size
        left = self.rect.x - border_size
        top = self.rect.y - border_size
        width = self.rect.width + border_size * 2
        height = self.rect.height + border_size * 2

        pygame.draw.rect(self.window, self.border_color,
                         (left, top, width, height), border_size)

    def touch(self, pos):
        return self.rect.collidepoint(pos)


class Button(Element):
    border_color = (55, 155, 55)

    def __init__(self, window, text, position, size, fill_color, text_color, text_size):
        super(Button, self).__init__(window, position, size, text, text_size, text_color)

        self.button = pygame.Surface(size).convert()
        self.button.fill(fill_color)

        self.border_color = Button.border_color

        self.rect = pygame.Rect(self.position, self.size)
        self.set_text(self.text)

    def draw(self):
        text_rect = self.text_font.get_rect(
            center=(self.button.get_width()/2, self.button.get_height()/2))
        self.button.blit(self.text_font, text_rect)
        self.window.blit(self.button, (self.rect.x, self.rect.y))

        self.draw_border()


class InputField(Element):
    border_color = (100, 100, 100)
    font_size = 15

    def __init__(self, window, position, size):
        super(InputField, self).__init__(window, position, size, "", InputField.font_size)

        self.active = False
        self.border_color = InputField.border_color

    def draw(self):
        self.field.fill(InputField.background_color)

        text = self.text
        if self.is_active():
            text = text + "|"

        # Text
        if text:
            font = pygame.font.Font(
                pygame.font.get_default_font(), self.text_size)
            text_font = font.render(text, True, self.text_color)

            text_rect = text_font.get_rect(
                midleft=(5, self.field.get_height()/2))
            self.field.blit(text_font, text_rect)

        self.window.blit(self.field, (self.rect.x, self.rect.y))

        self.draw_border()

    def activate(self):
        self.active = True
        self.draw()

    def is_active(self):
        return self.active

    def passivate(self):
        self.active = False
        self.draw()

    def add_char(self, char):
        if len(self.text) < 20:
            self.text += char
            self.draw()

    def remove_char(self):
        if self.text:
            self.text = self.text[:-1]
        self.draw()
