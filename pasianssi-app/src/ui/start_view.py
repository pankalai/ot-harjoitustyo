import pygame
from ui.klondike_view import KlondikeView
from ui.button import Button

class StartView:
    """
    Pelin alkunäkymä. 
    Käyttäjänimen antaminen ja vaikeustason valinta.
    """
    
    button_size = (115, 60)

    button_color = (114, 214, 114)
    text_color = (16,48,16)
    text_color2 = (59, 19, 19)

    header_font_size = 48
    text_font_size = 24

    def __init__(self, window, background_color):
        self.window = window
        self.width, self.height = window.get_size()

        self.background_color = background_color
        
        self.header_font = pygame.font.Font(None, StartView.header_font_size)
        self.text_font = pygame.font.Font(None, StartView.text_font_size)

    def _start(self):
        
        header = self.header_font.render('Tervetuloa pelaamaan Pasianssia!', True, StartView.text_color2)
        header_rect = header.get_rect(center=(self.width/2, self.height/3))

        # Window
        self.window.fill(self.background_color)

        # Header
        self.window.blit(header, header_rect)

        # Buttons
        top_pos = self.height/2
        button_easy = Button("Helppo",((self.width/2)*0.8-self.button_size[0]/2,top_pos),StartView.button_size,StartView.button_color,StartView.text_color)
        button_difficult = Button("Vaikea",((self.width/2)*1.2-self.button_size[0]/2,top_pos),StartView.button_size,StartView.button_color,StartView.text_color)

        button_easy.draw(self.window)
        button_difficult.draw(self.window)

        pygame.display.update()

        running = True
        level = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if button_easy.clicked(event.pos):
                        level = 1
                    elif button_difficult.clicked(event.pos):
                        level = 3

                if level:
                    self.window.fill(self.background_color)
                    pygame.display.update()
                    return level

        return None
