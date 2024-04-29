from entities.card_group import CardGroup
from entities.card import Card


class Pile(CardGroup):
    """Luokka pasianssipelin pinojen hallintaan.
    Args:
        CardGroup (_type_): perii CardGroup luokan
    """

    def get_sub_cards(self, card: Card):
        """Palauttaa pinossa olevan kortin ja sen päällä olevat kortit

        Args:
            card (Card): Card-luokan olio

        Returns:
            Lista, jossa haettava kortti ja sen päällä olevat kortit. 
            Jos korttia ei ole pinossa, niin tyhjä lista.
        """
        sub_cards = []
        try:
            index = self.cards.index(card)
        except ValueError:
            pass
        else:
            for i in range(index, len(self.cards)):
                sub_cards.append(self.cards[i])
        return sub_cards

    def update(self):
        """Kääntää pinon päällimmäisen kortin jos se on kuvapuoli alaspäin
        """
        if self.cards:
            top_card = self.cards[-1]
            if not top_card.show:
                top_card.flip()

    def __iter__(self):
        self.n_cards = 0
        return self

    def __next__(self):
        if self.n_cards < self.number_of_cards:
            card = self.cards[self.n_cards]
            self.n_cards += 1
            return card
        raise StopIteration
