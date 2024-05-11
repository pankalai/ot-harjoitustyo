import pygame
from ui.ui_settings import ui_settings


class Element:
    """Näkymän elementtien pääluokka.
    """

    def __init__(self, position=None, size=None, text="", text_size=None, text_color=None):
        self._position = position

        self._text = text
        self._text_color = text_color if text_color else ui_settings.text_color_element
        self._text_size = text_size if text_size else ui_settings.text_size_element

        self._font = pygame.font.Font(None, self._text_size)
        self._text_font = self._font.render(self._text, True, self._text_color)

        self._size = size if size else (
            self._text_font.get_rect().width, self._text_font.get_rect().height)

        self._field = pygame.Surface(self._size).convert()

        if self._position:
            self._set_rect()

    def set_text(self, text):
        self._text_font = self._font.render(text, True, self._text_color)

    def get_text(self):
        return self._text

    def set_underline(self):
        self._font.set_underline(True)
        self._text_font = self._font.render(
            self._text, True, self._text_color)

    def set_position(self, position):
        self._position = position
        self._set_rect()

    def get_position(self):
        return self._position

    def get_size(self):
        return self._size

    def draw(self, window):
        window.blit(self._text_font, self.rect)

    def _set_rect(self):
        self.rect = self._field.get_rect(
            center=(self._position[0], self._position[1]))

    def _draw_border(self, window):
        border_size = ui_settings.border_size
        left = self.rect.x - border_size
        top = self.rect.y - border_size
        width = self.rect.width + border_size * 2
        height = self.rect.height + border_size * 2

        pygame.draw.rect(window, self._border_color,
                         (left, top, width, height), border_size)

    def touch(self, pos):
        return self.rect.collidepoint(pos)


class Button(Element):
    """Painikkeista vastaava luokka.

    Args:
        Perii Element-luokan.
    """

    def __init__(self, text, position, size, fill_color, text_color, text_size):
        super(Button, self).__init__(
            position, size, text, text_size, text_color)

        self._border_color = ui_settings.border_color_button
        self.fill_color = fill_color

    def draw(self, window):
        self.rect = pygame.Rect(self._position, self._size)
        self._field.fill(self.fill_color)
        text_rect = self._text_font.get_rect(
            center=(self._field.get_width()/2, self._field.get_height()/2))
        self._field.blit(self._text_font, text_rect)
        window.blit(self._field, (self.rect.x, self.rect.y))

        self._draw_border(window)


class InputField(Element):
    """Syöttökentistä vastaava luokka.

    Args:
        Element (_type_): _description_
    """

    def __init__(self, position, size):
        super(InputField, self).__init__(
            position, size, "", ui_settings.input_text_size)

        self._active = False
        self._border_color = ui_settings.border_color_input_field

    def activate(self, window):
        self._active = True
        self.draw(window)

    def is_active(self):
        return self._active

    def passivate(self, window):
        self._active = False
        self.draw(window)

    def add_char(self, char, window):
        if len(self._text) < 20:
            self._text += char
            self.draw(window)

    def remove_char(self, window):
        if self._text:
            self._text = self._text[:-1]
        self.draw(window)

    def draw(self, window):
        self._field.fill(ui_settings.input_field_background)

        text = self._text
        if self.is_active():
            text = text + "|"

        # Text
        if text:
            text_font = self._font.render(text, True, self._text_color)

            text_rect = text_font.get_rect(
                midleft=(5, self._field.get_height()/2))
            self._field.blit(text_font, text_rect)

        window.blit(self._field, (self.rect.x, self.rect.y))

        self._draw_border(window)


class InfoBar:
    """Tietopalkista vastaava luokka.
    """

    def __init__(self):
        self._font = pygame.font.Font(
            pygame.font.get_default_font(), ui_settings.text_size_sub_bar)
        self._text_color = ui_settings.text_color_sub_bar

        self._set_rects()

    def _set_rects(self):
        surface = pygame.Surface((20, 20)).convert()
        self.time_rect = surface.get_rect(bottomright=(
            ui_settings.window_size[0]/1.15, ui_settings.window_size[1]))
        self.moves_rect = surface.get_rect(midbottom=(
            ui_settings.window_size[0]/2, ui_settings.window_size[1]))

    def update_info(self, time, moves):
        self._time = time
        self._moves = moves

    def draw(self, window):
        time_text = self._font.render(self._time, True, self._text_color)
        moves_text = self._font.render(
            "Siirrot: " + str(self._moves), True, self._text_color)
        window.blit(time_text, self.time_rect)
        window.blit(moves_text, self.moves_rect)
