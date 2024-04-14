from random import shuffle
from entities.card import Card


class Deck:
    def __init__(self, suits, values):
        self.cards = []
        self.suits = suits
        self.values = values
        self.build()
        self.n = len(self.cards)

    def build(self):
        self.cards.clear()
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(suit, value))

    def deal(self):
        if not self.cards:
            return None

        return self.cards.pop()

    def shuffle(self):
        shuffle(self.cards)

    @property
    def number_of_cards(self):
        return len(self.cards)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.cards):
            card = self.cards[self.n]
            self.n += 1
            return card
        raise StopIteration
