from random import shuffle
from entities.card import Card


class Deck:
    """Luokka, joka tarjoaa korttipakan toiminnallisuudet, kuten sekoittamisen ja jakamisen
    """

    def __init__(self, suits: list, ranks: list):
        """Luokan konstruktori, joka luo uuden korttipakan

        Args:
            suits (list): korttien maat
            ranks (list): korttien arvot
        """
        self.cards = []
        self.suits = suits
        self.ranks = ranks
        self.build()
        self.n_cards = self.number_of_cards

    def build(self):
        """Luo korteista uuden pakan
        """
        self.cards.clear()
        for suit in self.suits:
            for value in self.ranks:
                self.cards.append(Card(suit, value))

    def deal(self):
        """Jakaa päällimmäisen kortin pakasta

        Returns:
            Jos pakassa on kortteja, niin Cards-luokan olio, muussa tapauksessa None
        """
        if not self.cards:
            return None

        return self.cards.pop()

    def shuffle(self):
        """Sekoittaa pakan
        """
        shuffle(self.cards)

    @property
    def number_of_cards(self):
        """Palauttaa korttien määrän pakassa

        Returns:
            Korttien lukumäärä
        """
        return len(self.cards)

    def __iter__(self):
        self.n_cards = 0
        return self

    def __next__(self):
        if self.n_cards < self.number_of_cards:
            card = self.cards[self.n_cards]
            self.n_cards += 1
            return card
        raise StopIteration
