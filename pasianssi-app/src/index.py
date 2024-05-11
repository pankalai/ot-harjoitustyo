import pygame
from ui.ui_settings import ui_settings


def main():

    pygame.display.set_caption("Pasianssi")
    window = pygame.display.set_mode(ui_settings.window_size)
    pygame.init()

    # pygame init ennen importtia
    from ui.ui import UI

    ui = UI(window)
    ui.show()


if __name__ == "__main__":
    main()
