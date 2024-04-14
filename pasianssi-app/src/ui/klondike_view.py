import pygame
from services.klondike_service import Klondike
import time


class KlondikeView:
    """
    Klondiken näkymä. 
    """
    card_size = (75, 125)

    stack_position = (50, 50)
    waste_position = (150, 50)
    pile_position = (50, 200)
    foundation_position = (325, 50)

    waste_offset = card_size[0]*0.25
    pile_offset_left = card_size[0]*1.25
    pile_offset_top = card_size[0]*0.25
    foundation_offset = card_size[0]*1.25

    empty_stack_color = (0, 0, 255)
    empty_foundation_color = (255, 0, 0)

    def __init__(self, window, level):
        self.window = window
        self.game = Klondike(level)
        self.stack = pygame.sprite.Group()
        self.waste = pygame.sprite.LayeredUpdates()
        self.piles = pygame.sprite.LayeredUpdates()
        self.foundations = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.stack_area = pygame.Rect(KlondikeView.stack_position, KlondikeView.card_size)
        self.moving_object = None

        # actions
        self.dealing = False
        self.double_clicked = None

    def _start(self):
        self.game.prepare()
        
        # Set size of cards
        for card in self.game.deck:
            card.set_image_size(KlondikeView.card_size)

        self.game.draw()
        self._initialize_sprites()
        self._main_loop()

    def _initialize_sprites(self):
        
        # Piles
        left_pos = KlondikeView.pile_position[0]
        for i in range(len(self.game.piles)):
            top_pos = KlondikeView.pile_position[1]

            name = "pile" + str(i)
            setattr(self, name, pygame.sprite.Group())
            obj = getattr(self, name, None)

            for card in self.game.piles[i]:
                card.set_position((left_pos, top_pos))
                obj.add(card)
                top_pos += KlondikeView.pile_offset_top

            self.all_sprites.add(obj)
            left_pos += KlondikeView.pile_offset_left

        # Stack
        top_card = self.game.stack[-1]
        top_card.set_position(KlondikeView.stack_position)
        self.stack.add(self.game.stack[-1])
            
        self.all_sprites.add(self.stack)

    def _main_loop(self):
        self.click_time = 0
        while True:
            if self._handle_input() == False:
                break
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONUP:
                if time.time() - self.click_time < 0.5:
                    self.double_clicked = self._clicked_sprite(event)

                elif self.moving_object:
                    self.moving_object.sprite.rect.x = self.moving_object.x
                    self.moving_object.sprite.rect.y = self.moving_object.y

                self.moving_object = None
                self.click_time = time.time()

            elif event.type == pygame.MOUSEMOTION and self.moving_object:
                self.moving_object.sprite.rect.move_ip(event.rel)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # self.all_sprites.update()
                if event.button == 1:
                    # Stack
                    if self.stack_area.collidepoint(event.pos):
                        self.dealing = True

    def _game_logic(self):

        if self.dealing:
            self.game.deal()
            
            self.update_waste()

            self.all_sprites.remove(self.stack)
            self.stack.empty()
            if self.game.stack:
                top_card = self.game.stack[-1]
                top_card.set_position(KlondikeView.stack_position)
                self.stack.add(top_card)

            self.all_sprites.add(self.stack)

            self.dealing = False

        elif self.double_clicked:
            if self.game.add_to_foundation(self.double_clicked):
                self.double_clicked.kill()
                for i in range(len(self.game.foundations)):
                    for j in reversed(range(min(2, len(self.game.foundations[i])))):
                        card = self.game.foundations[i][-1-j]
                        card.set_position((KlondikeView.foundation_position[0]+KlondikeView.foundation_offset*i, KlondikeView.foundation_position[1]))
                        self.foundations.add(card)

                self.all_sprites.add(self.foundations)
                self.update_waste()

            self.double_clicked = None

        # Päivitä kortit
        self.all_sprites.update()

    def _draw(self):
        self.window.fill((0, 0, 0))

        # Stack empty
        if not self.game.stack:
            pygame.draw.rect(self.window, KlondikeView.empty_stack_color,
                             (KlondikeView.stack_position, KlondikeView.card_size), 1)

        # Foundation empty
        for i in range(len(self.game.foundations)):
            if not self.game.foundations[i]:
                pygame.draw.rect(self.window, KlondikeView.empty_foundation_color, ((
                    KlondikeView.foundation_position[0]+i*KlondikeView.foundation_offset, KlondikeView.foundation_position[1]), KlondikeView.card_size), 1)

        self.all_sprites.draw(self.window)
        self.waste.draw(self.window)
        pygame.display.update()

    def _clicked_sprite(self, event):
        # Piles
        for i in range(len(self.game.piles)):
            for card_sprite in reversed(list(getattr(self, "pile"+str(i)))):
                if card_sprite.rect.collidepoint(event.pos):
                    if not card_sprite.show:
                        return None
                    else:
                        return card_sprite
        # Waste
        if self.game.waste:
            card = list(self.waste)[-1]
            if card.rect.collidepoint(event.pos):
                return card

    def update_waste(self):
        self.all_sprites.remove(self.waste)

        self.waste.empty()
        for i, card in enumerate(self.game.get_waste_top_cards()):
            card.remove(self.stack)
            self.waste.add(card)
            card.set_position((KlondikeView.waste_position[0]+i*KlondikeView.waste_offset,KlondikeView.waste_position[1]))
            self.waste.move_to_front(card)

        self.all_sprites.add(self.waste)