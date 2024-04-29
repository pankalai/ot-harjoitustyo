import pygame
from entities.card import Card


class CardGroup(pygame.sprite.Sprite):
    """Luokka jonka avulla hallitaan korttiryhmää

    Args:
        Perii pygamen sprite-luokan
    """

    def __init__(self):
        """ Luokan konstruktori, joka luo uuden korttiryhmän.
        """
        super().__init__()
        self.cards = []
        self.rect = None
        self.n_cards = None

    def clear(self):
        """Tyhjentää korttiryhmän
        """
        self.cards.clear()

    def set_rect(self, pos: tuple, size: tuple):
        """Asettaa korttiryhmän suorakulmaiset koordinaatit

        Args:
            pos (_type_): sijainti tuplena (vasen,ylä)
            size (_type_): koko tuplena (leveys, korkeus)
        """
        self.rect = pygame.Rect(pos, size)

    def reverse(self):
        """Kääntää korttien järjestyksen
        """
        self.cards.reverse()

    def is_empty(self):
        """Palauttaa tiedon, onko korttiryhmä tyhjä

        Returns:
            True, jos korttiryhmässä ei ole kortteja
        """
        return len(self.cards) == 0

    def contains_card(self, card: Card):
        """Palauttaa tiedon, sisältääkö korttiryhmä tietyn kortin

        Args:
            card (Card): Card-luokan olio

        Returns:
            True, jos kortti on ryhmässä
        """
        return card in self.cards

    def add(self, card: Card):
        """Lisää kortin ryhmään

        Args:
            card (Card): Card-luokan olio
        """
        self.cards.append(card)

    def remove(self, card: Card):
        """Poistaa kortin ryhmästä jos se löytyy ryhmästä

        Args:
            card (Card): Card-luokan olio
        """
        if self.contains_card(card):
            self.cards.remove(card)

    def get_top_cards(self, number=1):
        """Palauttaa ryhmään viimeksi lisätyt kortit

        Args:
            number (int, optional): palautettavien korttien määrä, oletusarvo 1

        Returns:
            Argumentin mukainen määrä kortteja listana. 
            Palautettavien korttien määrä on korkeintaan yhtä suuri kuin 
            ryhmässä olevien korttien määrä.
        """
        return [self.cards[-1-i] for i in reversed(range(min(number, len(self.cards))))]

    @property
    def number_of_cards(self):
        """Kertoo ryhmässä olevien korttien määrän

        Returns:
            Korttien lukumäärä
        """
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
