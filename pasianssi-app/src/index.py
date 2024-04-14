import pygame
from ui.ui import UI


def main():

    pygame.init()
    window_size = (750, 500)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pasianssi")
    game = UI(window)
    game.start()


if __name__ == "__main__":
    main()
