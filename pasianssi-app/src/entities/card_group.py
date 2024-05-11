import pygame
from entities.card import Card


class CardGroup(pygame.sprite.Sprite):
    """Luokka jonka avulla hallitaan korttiryhmää.

    Args:
        Perii pygamen sprite-luokan.
    """

    def __init__(self):
        """ Luokan konstruktori, joka luo uuden korttiryhmän.
        """
        super().__init__()
        self._cards = []
        self.rect = None
        self._n_cards = None

    def as_list(self):
        """Palauttaa korttiryhmän listana.

        Returns:
            Lista kortteja.
        """
        return self._cards

    def bottom_card(self):
        """Palauttaa korttiryhmän alimman kortin.

        Returns:
            Card-luokan olio, jos korttiryhmässä on kortteja, muuten None.
        """
        if self._cards:
            return self._cards[0]
        return None

    def card_index(self, card: Card):
        """Palauttaa kortin indeksin ryhmässä.

        Args:
            card (Card): Haettava kortti.

        Returns:
            Kortin indeksi.
        """
        return self._cards.index(card)

    def clear(self):
        """Tyhjentää korttiryhmän.
        """
        self._cards.clear()

    def set_rect(self, pos: tuple, size: tuple):
        """Asettaa korttiryhmän suorakulmaiset koordinaatit.

        Args:
            pos (tuple): Sijainti (vasen, ylä).
            size (tuple): Koko (leveys, korkeus).
        """
        self.rect = pygame.Rect(pos, size)

    def get_position(self):
        """Palauttaa korttiryhmän sijainnin.

        Returns:
            Korttiryhmän x- ja y-koordinaatti.
        """
        return self.rect.x, self.rect.y

    def reverse(self):
        """Kääntää korttien järjestyksen.
        """
        self._cards.reverse()

    def is_empty(self):
        """Palauttaa tiedon, onko korttiryhmä tyhjä.

        Returns:
            True, jos korttiryhmässä ei ole kortteja.
        """
        return len(self._cards) == 0

    def contains_card(self, card: Card):
        """Palauttaa tiedon, sisältääkö korttiryhmä tietyn kortin.

        Args:
            card (Card): Card-luokan olio.

        Returns:
            True, jos kortti on ryhmässä.
        """
        return card in self._cards

    def add(self, card: Card):
        """Lisää kortin ryhmään.

        Args:
            card (Card): Card-luokan olio.
        """
        self._cards.append(card)

    def remove(self, card: Card):
        """Poistaa kortin ryhmästä jos se löytyy ryhmästä.

        Args:
            card (Card): Card-luokan olio.
        """
        if self.contains_card(card):
            self._cards.remove(card)

    def get_top_cards(self, number=1):
        """Palauttaa ryhmään viimeksi lisätyt kortit.

        Args:
            number (int, optional): palautettavien korttien määrä, oletusarvo 1.

        Returns:
            Argumentin mukainen määrä kortteja listana.
            Palautettavien korttien määrä on korkeintaan yhtä suuri kuin
            ryhmässä olevien korttien määrä.
        """
        return [self._cards[-1-i] for i in reversed(range(min(number, len(self._cards))))]

    @property
    def number_of_cards(self):
        """Kertoo ryhmässä olevien korttien määrän.

        Returns:
            Korttien lukumäärä.
        """
        return len(self._cards)

    def __iter__(self):
        self._n_cards = self.number_of_cards-1
        return self

    def __next__(self):
        if self._n_cards >= 0:
            card = self._cards[self._n_cards]
            self._n_cards -= 1
            return card
        raise StopIteration
