import pygame

def main():    

    pygame.init()
    window_size = (500, 300)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pasianssi")

    # Painikkeet pelin eri tasoille
    font = pygame.font.Font(None, 24)

    button_color = (117,223,134)

    button_surface1 = pygame.Surface((100, 75))
    button_surface2 = pygame.Surface((100, 75))
    
    button_surface1.fill(button_color)
    button_surface2.fill(button_color)

    text_color = (59,73,61)
    text1 = font.render("Helppo", True, text_color)
    text2 = font.render("Vaikea", True, text_color)
    
    text_rect1 = text1.get_rect(center=(button_surface1.get_width()/2, button_surface1.get_height()/2))
    text_rect2 = text2.get_rect(center=(button_surface2.get_width()/2, button_surface2.get_height()/2))

    button_level1_rect = pygame.Rect(100, 125, 150, 50)
    button_level2_rect = pygame.Rect(275, 125, 150, 50)

    window.fill((255, 255, 255))
    
    button_surface1.blit(text1, text_rect1)
    button_surface2.blit(text2, text_rect2)

    window.blit(button_surface1, (button_level1_rect.x, button_level1_rect.y))
    window.blit(button_surface2, (button_level2_rect.x, button_level2_rect.y))

    run = True
    while run:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                run = False

        pygame.display.update()

if __name__ == "__main__":
    main()


        

