from random import shuffle
from entities.card import Card


class Deck:
    """Luokka, joka tarjoaa korttipakan toiminnallisuudet, kuten sekoittamisen ja jakamisen.
    """

    def __init__(self, suits: list, ranks: list):
        """Luokan konstruktori, joka luo uuden korttipakan.

        Args:
            suits (list): Korttien maat.
            ranks (list): Korttien arvot.
        """
        self._cards = []
        self._suits = suits
        self._ranks = ranks
        self._n_cards = self.number_of_cards

        self.build()

    def build(self):
        """Luo korteista uuden pakan.
        """
        self._cards.clear()
        for suit in self._suits:
            for value in self._ranks:
                self._cards.append(Card(suit, value))

    def deal(self):
        """Jakaa päällimmäisen kortin pakasta.

        Returns:
            Jos pakassa on kortteja, niin Cards-luokan olio, muussa tapauksessa None.
        """
        if not self._cards:
            return None

        return self._cards.pop()

    def shuffle(self):
        """Sekoittaa pakan.
        """
        shuffle(self._cards)

    @property
    def number_of_cards(self):
        """Palauttaa korttien määrän pakassa.

        Returns:
            Korttien lukumäärä.
        """
        return len(self._cards)

    def __iter__(self):
        self._n_cards = 0
        return self

    def __next__(self):
        if self._n_cards < self.number_of_cards:
            card = self._cards[self._n_cards]
            self._n_cards += 1
            return card
        raise StopIteration
