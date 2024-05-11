from entities.card_group import CardGroup
from entities.card import Card


class Pile(CardGroup):
    """Luokka pasianssipelin pinojen hallintaan.
    Args:
        Perii CardGroup luokan
    """

    def get_cards_on_top_of(self, card: Card):
        """Palauttaa kortin päällä olevat kortit.

        Args:
            card (Card): Card-luokan olio.

        Returns:
            Kortin päällä olevat kortit listana.
            Tyhjä lista, jos korttia ei ole pinossa.
        """
        top_cards = []
        try:
            index = self.card_index(card)
        except ValueError:
            pass
        else:
            for i in range(index+1, len(self._cards)):
                top_cards.append(self._cards[i])
        return top_cards

    def __iter__(self):
        self._n_cards = 0
        return self

    def __next__(self):
        if self._n_cards < self.number_of_cards:
            card = self._cards[self._n_cards]
            self._n_cards += 1
            return card
        raise StopIteration
