import os
import pygame
from services.klondike_service import Klondike
from entities.grabbed_cards import GrabbedCards
import time

dirname = os.path.dirname(__file__)


class KlondikeView:
    """
    Klondiken näkymä. 
    """
    card_size = (75, 110)

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

    font_color = (55, 55, 55)
    font_size = 15

    def __init__(self, window, background_color, clock):
        self.window = window
        self.background_color = background_color

        self.game = Klondike()
        self.moves = 0

        self._clock = clock
        self.font = pygame.font.Font(
            pygame.font.get_default_font(), KlondikeView.font_size)
        self.text = self.font.render("", True, KlondikeView.font_color)
        self.time_rect = self.text.get_rect(bottomright=(
            self.window.get_width()/1.15, self.window.get_height()))
        self.moves_rect = self.text.get_rect(midbottom=(
            self.window.get_width()/2, self.window.get_height()))

        self.waste = pygame.sprite.LayeredUpdates()

        self.piles_area = pygame.sprite.Group()
        self.piles_cards = pygame.sprite.LayeredUpdates()

        self.foundations_area = pygame.sprite.Group()
        self.foundations_cards = pygame.sprite.Group()

        self.stack_area = pygame.Rect(
            KlondikeView.stack_position, KlondikeView.card_size)

        # Moving object
        self.grabbed_cards_list = []
        self.grabbed_cards = GrabbedCards()

        # Actions
        self.dealing = False
        self.double_clicked = None
        self.update_foundations_flag = False
        self.update_piles_flag = False
        self.update_waste_flag = False

    def _play(self, start_new=True, level=None):
        if start_new:
            self.game.set_level(level)
            self.game.prepare()

            # Set size of cards
            for card in self.game.deck:
                card.set_image_size(KlondikeView.card_size)

            self.game.draw()
            self._initialize_sprites()

            self._clock.start_clock()

        self._main_loop()

        return self.game.game_won()

    def _initialize_infobar(self):
        pass

    def _initialize_sprites(self):

        self.waste.empty()
        self.foundations_cards.empty()
        self.piles_cards.empty()

        # Create rects of foundations
        left_pos, top_pos = KlondikeView.foundation_position
        for foundation in self.game.foundations:
            foundation.set_rect((left_pos, top_pos), KlondikeView.card_size)
            left_pos += KlondikeView.foundation_offset

            self.foundations_area.add(foundation)

        # Create rects of piles
        # the height of pile is set to the bottom of the window
        left_pos, top_pos = KlondikeView.pile_position
        for pile in self.game.piles:
            pile.set_rect(
                (left_pos, top_pos), (KlondikeView.card_size[0], self.window.get_height()-top_pos))
            left_pos += KlondikeView.pile_offset_left

            self.piles_area.add(pile)

        # Create piles
        self.update_piles()

        # Stack image
        image = pygame.image.load(
            os.path.join(dirname, "..", r"assets/cards", "back-side.png")
        )
        self.stack_image = pygame.transform.smoothscale(
            image, KlondikeView.card_size)
        self.stack_rect = pygame.Rect(
            KlondikeView.stack_position, KlondikeView.card_size)

    def _main_loop(self):
        self.click_time = 0

        while not self.game.game_won():
            if self._handle_events() == False:
                break
            self._draw()
            self._clock.tick(60)

    def _handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONUP:
                if time.time() - self.click_time < 0.5:
                    self.double_clicked = self._clicked_sprite(event.pos, True)
                    if self.double_clicked:
                        self._handle_double_click()

                elif not self.grabbed_cards.is_empty():
                    self._check_collision(self.grabbed_cards.bottom_card())

                self.grabbed_cards.clear()
                self.click_time = time.time()

            elif event.type == pygame.MOUSEMOTION and self.grabbed_cards:
                self.grabbed_cards.move(event.rel)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.stack_area.collidepoint(event.pos):
                    self.game.deal()
                    self.update_waste_flag = True
                else:
                    card = self._clicked_sprite(event.pos)
                    if card:
                        self.create_grabbed_object(card)

        if self.update_piles_flag:
            self.update_piles()
            self.update_piles_flag = False

        if self.update_foundations_flag:
            self.update_foundations()
            self.update_foundations_flag = False

        if self.update_waste_flag:
            self.update_waste()
            self.update_waste_flag = False

    def _draw(self):
        self.window.fill(self.background_color)

        # Stack
        if self.game.stack_is_empty():
            pygame.draw.rect(self.window, KlondikeView.empty_stack_color,
                             (KlondikeView.stack_position, KlondikeView.card_size), 1)
        else:
            self.window.blit(self.stack_image, self.stack_rect)

        # Foundations
        for i, foundation in enumerate(self.game.foundations):
            if foundation.is_empty():
                pygame.draw.rect(self.window, KlondikeView.empty_foundation_color, ((
                    KlondikeView.foundation_position[0]+i*KlondikeView.foundation_offset, KlondikeView.foundation_position[1]), KlondikeView.card_size), 1)

        self.foundations_cards.draw(self.window)
        self.waste.draw(self.window)
        self.piles_cards.draw(self.window)

        # Clock
        self.time_text = self.font.render(
            self._clock.elapsed_time(), True, KlondikeView.font_color)
        self.window.blit(self.time_text, self.time_rect)

        # Moves
        self.moves_text = self.font.render(
            "Siirrot: " + str(self.moves), True, KlondikeView.font_color)
        self.window.blit(self.moves_text, self.moves_rect)

        pygame.display.update()

    def _handle_double_click(self):
        if self.game.add_to_foundation(self.double_clicked):
            self.double_clicked.kill()
            self.update_foundations_flag = True
            self.moves += 1

        self.update_waste_flag = True
        self.update_piles_flag = True

        self.double_clicked = None

    def _clicked_sprite(self, position, double_click=False):
        # Waste

        cards = self.game.get_waste_top_cards()
        if cards:
            if cards[-1].rect.collidepoint(position):
                return cards[-1]

        # Piles and foundations
        found_card = None
        for pile in self.game.piles:
            for card in pile:
                if card.rect.collidepoint(position) and card.show:
                    found_card = card
            if found_card:
                return found_card

        # Foundation
        if not double_click:
            for foundation in self.game.foundations:
                for card in foundation:
                    if card.rect.collidepoint(position):
                        return card

    def create_grabbed_object(self, card):
        grabbed_cards_list = self.game.get_sub_cards(card)
        for card in grabbed_cards_list:
            self.piles_cards.add(card)
            self.piles_cards.move_to_front(card)
            self.grabbed_cards.add(card)

    def _check_collision(self, sprite):
        move_accepted = False

        # Piles
        for pile in self.piles_area:
            if pygame.sprite.collide_rect(sprite, pile):
                if self.game.add_to_pile(self.grabbed_cards.get_list(), pile):
                    move_accepted = True
                    break

        # Foundations
        if not move_accepted:
            for foundation in self.foundations_area:
                if pygame.sprite.collide_rect(sprite, foundation):
                    if self.game.add_to_foundation(self.grabbed_cards.get_list(), foundation):
                        break

        if move_accepted:
            self.moves += 1

        self.update_foundations_flag = True
        self.update_piles_flag = True
        self.update_waste_flag = True

    def update_waste(self):
        self.waste.empty()
        for i, card in enumerate(self.game.get_waste_top_cards()):
            self.waste.add(card)
            card.set_position(
                (KlondikeView.waste_position[0]+i*KlondikeView.waste_offset, KlondikeView.waste_position[1]))
            self.waste.move_to_front(card)

        self.waste.update()

    def update_foundations(self):
        self.foundations_cards.empty()

        left_pos, top_pos = KlondikeView.foundation_position
        for foundation in self.game.foundations:
            for card in self.game.get_foundation_top_cards(foundation):
                card.set_position((left_pos, top_pos))
                self.foundations_cards.add(card)

            left_pos += KlondikeView.foundation_offset

    def update_piles(self):
        # Piles
        for pile in self.game.piles:
            pile.update()

        self.piles_cards.empty()

        left_pos = KlondikeView.pile_position[0]
        for pile in self.game.piles:
            top_pos = KlondikeView.pile_position[1]
            for card in pile:
                card.set_position((left_pos, top_pos))
                top_pos += KlondikeView.pile_offset_top
                self.piles_cards.add(card)
            left_pos += KlondikeView.pile_offset_left

        self.piles_cards.update()
