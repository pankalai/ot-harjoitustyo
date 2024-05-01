from ui.ui import UI
from services.clock import Clock
from services.game_loop import GameLoop
import pygame

window_size = (750, 500)

def main():

    pygame.init()
    pygame.display.set_caption("Pasianssi")
    window = pygame.display.set_mode(window_size)
    
    game = UI(window)
    game.start()


if __name__ == "__main__":
    main()
