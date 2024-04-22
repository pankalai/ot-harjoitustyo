import pygame


class CardGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.rect = None
        self.n_cards = None

    def set_rect(self, pos, size):
        self.rect = pygame.Rect(pos, size)

    def reverse(self):
        self.cards.reverse()

    def is_empty(self):
        return len(self.cards) == 0

    def contains_card(self, card):
        return card in self.cards

    def add(self, card):
        self.cards.append(card)
        return True

    def remove(self, card):
        if self.contains_card(card):
            self.cards.remove(card)

    def get_top_cards(self, number=1):
        return [self.cards[-1-i] for i in reversed(range(min(number, len(self.cards))))]

    @property
    def number_of_cards(self):
        return len(self.cards)

    def __iter__(self):
        self.n_cards = self.number_of_cards-1
        return self

    def __next__(self):
        if self.n_cards >= 0:
            card = self.cards[self.n_cards]
            self.n_cards -= 1
            return card
        raise StopIteration
