import pygame
from ui.klondike_view import KlondikeView

class StartView:
    """
    Pelin alkunäkymä. 
    Käyttäjänimen ja vaikeustason valinta.
    """

    def __init__(self, window):
        self.window = window
        self.width, self.height = window.get_size()

    def _start(self):
        font = pygame.font.Font(None, 24)

        button_color = (117, 223, 134)

        button_surface1 = pygame.Surface((100, 75))
        button_surface2 = pygame.Surface((100, 75))

        button_surface1.fill(button_color)
        button_surface2.fill(button_color)

        text_color = (59, 73, 61)
        text1 = font.render("Helppo", True, text_color)
        text2 = font.render("Vaikea", True, text_color)

        text_rect1 = text1.get_rect(
            center=(button_surface1.get_width()/2, button_surface1.get_height()/2))
        text_rect2 = text2.get_rect(
            center=(button_surface2.get_width()/2, button_surface2.get_height()/2))

        button_width = 150
        button_height = 50
        button_level1_rect = pygame.Rect((self.width/2)*0.85-button_width/2, (self.height/2), button_width, button_height)
        button_level2_rect = pygame.Rect((self.width/2)*1.15, (self.height/2), button_width, button_height)

        self.window.fill((0, 0, 0))

        button_surface1.blit(text1, text_rect1)
        button_surface2.blit(text2, text_rect2)

        self.window.blit(
            button_surface1, (button_level1_rect.x, button_level1_rect.y))
        self.window.blit(
            button_surface2, (button_level2_rect.x, button_level2_rect.y))

        pygame.display.update()

        running = True
        level = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if button_level1_rect.collidepoint(event.pos):
                        level = 1
                    if button_level2_rect.collidepoint(event.pos):
                        level = 3

                if level:
                    self.window.fill((0, 0, 0))
                    pygame.display.update()
                    return level        

            

        return None
