from entities.deck import Deck


class Klondike:
    """
    Klondike-pelin logiikasta vastaava luokka
    """
    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
    ranks = range(1, 14)

    def __init__(self, level=3):
        self.deck = Deck(Klondike.suits, Klondike.ranks)
        self.piles = [[] for _ in range(7)]
        self.foundations = [[] for _ in range(4)]
        self.stack = []
        self.waste = []

        if level == 1:
            self.turning_cards = 1
        elif level == 3:
            self.turning_cards = 3

    def prepare(self):
        self.deck.shuffle()

    def draw(self):
        pile_n = 1
        for pile in self.piles:
            for i in range(pile_n):
                card = self.deck.deal()
                pile.append(card)
                if i == pile_n-1:
                    card.flip()
            pile_n += 1

        self.stack = self.deck.cards.copy()

    def deal(self):
        if self.stack:
            for _ in range(min(self.turning_cards, len(self.stack))):
                card = self.stack.pop()
                self.waste.append(card)
                card.flip()
        else:
            for card in reversed(self.waste):
                card.flip()
                self.stack.append(card)
            self.waste.clear()

    def add_to_foundation(self, card, foundation_index=None):
        index = -1
        if foundation_index:
            if self.card_valid_for_foundation(card, foundation_index):
                self.foundations[foundation_index].append(card)
                index = foundation_index
        else:
            for i, foundation in enumerate(self.foundations):
                if self.card_valid_for_foundation(card, i):
                    foundation.append(card)
                    index = i
                    break

        if index >= 0:
            if not self.remove_card_from_foundation_or_pile(self.piles, card) and self.waste:
                if self.waste[-1] == card:
                    self.waste.pop()
            self.update_piles()
            return True

        return False

    def add_to_pile(self, cards, pile_index):
        if self.card_valid_for_pile(cards[0], pile_index):
            for card in cards:
                self.piles[pile_index].append(card)
            self.update_piles()
            return True

        return False

    def card_valid_for_foundation(self, card, foundation_index):
        if not self.foundations[foundation_index]:
            if card.rank == 1:
                return True
        elif (self.foundations[foundation_index][-1].suit == card.suit
              and self.foundations[foundation_index][-1].rank == card.rank-1):
            return True

        return False

    def card_valid_for_pile(self, card, pile_index):
        if not self.piles[pile_index]:
            if card.rank == 13:
                return True
        elif (self.piles[pile_index][-1].rank == card.rank+1 and
              self.piles[pile_index][-1].color != card.color):
            return True

        return False

    def update_piles(self):
        for pile in self.piles:
            if pile:
                top_card = pile[-1]
                if not top_card.show:
                    top_card.flip()

    def remove_card_from_foundation_or_pile(self, card_lists, card):
        found = False
        for card_list in card_lists:
            for item in card_list:
                if item == card:
                    card_list.remove(item)
                    found = True
                    break
            if found:
                return True
        return False

    def get_waste_top_cards(self):
        return [self.waste[-1-i] for i in reversed(range(min(3,len(self.waste))))]
