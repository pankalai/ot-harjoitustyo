import pygame
from ui.element import Button


class MessageBox:
    window_size = (350, 200)
    header_font_size = 28
    button_size = (110, 25)
    button_color = (114, 214, 114)
    text_color = (16, 48, 16)

    def __init__(self, window, won=False):

        self.window = window
        self.width, self.height = MessageBox.window_size

        top_pos = self.height/1.5
        text_size = 12
        self.button_quit = Button(self.window, "Palaa alkuun", ((
            self.width/2)*0.65-self.button_size[0]/2, top_pos), MessageBox.button_size, MessageBox.button_color, MessageBox.text_color, text_size)
        self.button_continue = Button(self.window, "Jatka pelaamista", ((
            self.width/2)*1.35-self.button_size[0]/2, top_pos), MessageBox.button_size, MessageBox.button_color, MessageBox.text_color, text_size)

        self.question_text = None
        self.button1_text = "Palaa alkuun"
        self.button2_text = None

        self.header_font = pygame.font.Font(None, MessageBox.header_font_size)

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

        self.won = None
        self._set_texts(won)

    def _set_texts(self, won):
        if not self.won or won != self.won:
            self.question_text = self.texts[won]["question_text"]
            self.button_continue.set_text(self.texts[won]["button2_text"])
            self.won = won

    def _show(self):
        pygame.display.set_mode(MessageBox.window_size)

        self.window.fill((219, 219, 200))

        # Header
        header = self.header_font.render(
            self.question_text, True, (59, 19, 19))
        header_rect = header.get_rect(center=(self.width/2, self.height/3))
        self.window.blit(header, header_rect)

        # Buttons
        self.button_quit.draw(self.window)
        self.button_continue.draw(self.window)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.button_quit.clicked(event.pos):
                        return True
                    elif self.button_continue.clicked(event.pos):
                        return False
