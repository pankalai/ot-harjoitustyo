import pygame
from ui.ui_settings import ui_settings
from ui.ui import UI


def main():

    pygame.display.set_caption("Pasianssi")
    window = pygame.display.set_mode(ui_settings.window_size)
    pygame.init()

    ui = UI(window)
    ui.show()


if __name__ == "__main__":
    main()
