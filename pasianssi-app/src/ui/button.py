import pygame


class Button:
    border_color = (255, 255, 255)

    def __init__(self, text, position, size, fill_color, text_color, border=True):
        self.position = position
        self.size = size

        self.button = pygame.Surface(size).convert()
        self.button.fill(fill_color)
        self.border = border

        self.rect = pygame.Rect(self.position, self.size)

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text = font.render(text, True, text_color)

    def draw(self, screen):
        text_rect = self.text.get_rect(
            center=(self.button.get_width()/2, self.button.get_height()/2))
        self.button.blit(self.text, text_rect)
        screen.blit(self.button, (self.rect.x, self.rect.y))

        if self.border:
            thickness = 1
            posx = self.position[0] - thickness
            posy = self.position[1] - thickness
            sizex = self.size[0] + thickness * 2
            sizey = self.size[1] + thickness * 2

            pygame.draw.rect(screen, Button.border_color,
                             (posx, posy, sizex, sizey), thickness)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
