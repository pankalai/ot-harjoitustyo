from entities.deck import Deck
from entities.card import Card
from entities.card_group import CardGroup
from entities.pile import Pile
from entities.group_handler import GroupHandler


class Klondike:
    """
    Klondike-pelin logiikasta vastaava luokka
    """
    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
    ranks = range(1, 14)

    def __init__(self, level=3, group_handler=GroupHandler()):
        self.deck = Deck(Klondike.suits, Klondike.ranks)

        self.piles = [Pile() for _ in range(7)]
        self.foundations = [CardGroup() for _ in range(4)]
        self.stack = CardGroup()
        self.waste = CardGroup()

        self.group_handler = group_handler

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
                self.group_handler.add_to_group(card, pile)
                if i == pile_n-1:
                    card.flip()
            pile_n += 1

        for card in self.deck:
            self.group_handler.add_to_group(card, self.stack)

        self.stack.reverse()

    def deal(self):
        if not self.stack.is_empty():
            for _ in range(min(self.turning_cards, self.stack.number_of_cards)):
                card = self.stack.get_top_cards(1)[0]
                self.group_handler.add_to_group(card, self.waste)
                card.flip()
        else:
            for card in self.waste:
                self.group_handler.add_to_group(card, self.stack)
                card.flip()

    def add_to_pile(self, card_list, pile):
        if self.valid_to_pile(card_list[0], pile):
            for card in card_list:
                self.group_handler.add_to_group(card, pile)
            return True
        return False

    def add_to_foundation(self, card, foundation=None):
        if isinstance(card, list):
            if len(card) > 1:
                return False
            card = card[0]

        if not isinstance(card, Card):
            return False

        if foundation:
            if self.valid_to_foundation(card, foundation):
                self.group_handler.add_to_group(card, foundation)
                return True
        else:
            for fnd in self.foundations:
                if self.valid_to_foundation(card, fnd):
                    self.group_handler.add_to_group(card, fnd)
                    return True
        return False

    def valid_to_pile(self, card, pile):
        if pile.is_empty():
            return card.rank == 13

        top_card = pile.get_top_cards(1)[0]
        if top_card.color != card.color and top_card.rank == card.rank+1:
            return True
        return False

    def valid_to_foundation(self, card, foundation):
        if foundation.is_empty():
            if card.rank == 1:
                return True
            return False
        top_card = foundation.get_top_cards(1)[0]
        return top_card.suit == card.suit and top_card.rank == card.rank-1

    def get_card_group(self, card):
        return self.group_handler.get_current_group(card)

    def get_waste_top_cards(self):
        return self.waste.get_top_cards(3)

    def get_foundation_top_cards(self, foundation):
        return foundation.get_top_cards(2)

    def get_sub_cards(self, card):
        group = self.group_handler.get_current_group(card)
        if isinstance(group, Pile):
            return group.get_sub_cards(card)
        return [card]

    def stack_is_empty(self):
        return self.stack.is_empty()

    def game_won(self):
        return not (False in [group.number_of_cards == 13 for group in self.foundations])
