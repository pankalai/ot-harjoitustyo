from entities.card_group import CardGroup


class Pile(CardGroup):

    def get_sub_cards(self, card):
        sub_cards = []
        index = self.cards.index(card)
        for i in range(index, len(self.cards)):
            sub_cards.append(self.cards[i])
        return sub_cards

    def update(self):
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
