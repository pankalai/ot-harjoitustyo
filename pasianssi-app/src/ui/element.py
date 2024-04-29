import pygame


class Element:
    def __init__(self, window) -> None:
        self.window = window
        self.border_color = None
        self.rect = None

    def draw_border(self):
        border_size = 1
        left = self.rect.x - border_size
        top = self.rect.y - border_size
        width = self.rect.width + border_size * 2
        height = self.rect.height + border_size * 2

        pygame.draw.rect(self.window, self.border_color,
                         (left, top, width, height), border_size)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Button(Element):
    border_color = (55, 155, 55)

    def __init__(self, window, text, position, size, fill_color, text_color, text_size=20, border=True):
        super(Button, self).__init__(window)
        self.position = position
        self.size = size

        self.text_size = text_size
        self.button = pygame.Surface(size).convert()
        self.button.fill(fill_color)

        self.border = border
        self.border_color = Button.border_color

        self.rect = pygame.Rect(self.position, self.size)

        self.text_color = text_color
        self.set_text(text)

    def set_text(self, text):
        font = pygame.font.Font(pygame.font.get_default_font(), self.text_size)
        self.text = font.render(text, True, self.text_color)

    def draw(self, screen):
        text_rect = self.text.get_rect(
            center=(self.button.get_width()/2, self.button.get_height()/2))
        self.button.blit(self.text, text_rect)
        screen.blit(self.button, (self.rect.x, self.rect.y))

        self.draw_border()


class InputField(Element):
    border_color = (100, 100, 100)
    text_color = (5, 5, 5)
    background_color = (219, 219, 219)
    text_size = 15

    def __init__(self, window, position, size):
        super(InputField, self).__init__(window)

        self.position = position
        self.size = size
        self.window = window

        self.field = pygame.Surface(size).convert()
        self.rect = self.field.get_rect(
            center=(self.position[0], self.position[1]))

        self.active = False

        self.text = ""
        self.font = pygame.font.Font(
            pygame.font.get_default_font(), InputField.text_size)
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
        self.text = self.text[:-1]
        self.draw()
