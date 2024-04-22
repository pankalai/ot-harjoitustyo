import unittest
from services.klondike_service import Klondike
from entities.deck import Deck
from entities.card import Card


class TestKlondike(unittest.TestCase):
    def setUp(self):
        self.klondike = Klondike(3)
        self.klondike.draw()

    def test_after_draw_piles_are_filled(self):
        n = 1
        for pile in self.klondike.piles:
            self.assertEqual(pile.number_of_cards, n)
            n += 1

    def test_after_draw_foundations_are_empty(self):
        for foundation in self.klondike.foundations:
            self.assertEqual(foundation.number_of_cards, 0)

    def test_after_draw_stock_includes_24_cards(self):
        self.assertEqual(self.klondike.stack.number_of_cards, 24)

    def test_after_all_cards_are_dealt_stock_is_empty_and_waste_full(self):
        for _ in range(int(self.klondike.stack.number_of_cards/self.klondike.turning_cards)):
            self.klondike.deal()

        self.assertEqual(self.klondike.stack.number_of_cards, 0)

    def test_can_add_ace_to_empty_foundation(self):
        card = Card("Spades", 1)
        self.assertEqual(self.klondike.add_to_foundation(card, 0), True)

    def test_cannot_add_other_than_ace_to_empty_foundation(self):
        card = Card("Clubs", 3)
        self.assertEqual(self.klondike.add_to_foundation(card, None), False)

    def test_can_add_rank_one_greater_to_foundation(self):
        card1 = Card("Spades", 1)
        card2 = Card("Spades", 2)
        pile = self.klondike.foundations[0]
        self.klondike.add_to_foundation(card1, pile)
        self.assertEqual(self.klondike.add_to_foundation(card2, None), True)

    def test_can_add_valid_card_on_pile(self):
        cards = []
        i = 0
        while True:
            card = self.klondike.piles[i].get_top_cards(1)[0]
            if card.rank != 1:
                rank = card.rank-1
                if card.suit in ("Diamonds", "Hearts"):
                    suit = "Spades"
                else:
                    suit = "Diamonds"
                break
            i += 1
        cards.append(Card(suit, rank))
        self.assertEqual(self.klondike.add_to_pile(
            cards, self.klondike.piles[i]), True)
        self.assertEqual(self.klondike.add_to_pile(
            cards, self.klondike.piles[i]), False)

    def test_can_add_only_king_on_empty_pile(self):
        pile1 = self.klondike.piles[0]
        pile1.cards.clear()
        pile2 = self.klondike.piles[1]
        pile2.cards.clear()
        self.assertEqual(self.klondike.add_to_pile(
            [Card("Spades", 13)], pile1), True)
        self.assertEqual(self.klondike.add_to_pile(
            [Card("Spades", 3)], pile2), False)

    def test_first_card_of_stack_remains_same_if_no_moves(self):
        first_card1 = self.klondike.stack.get_top_cards(1)[0]
        for _ in range(int(self.klondike.stack.number_of_cards/self.klondike.turning_cards)+1):
            self.klondike.deal()
        first_card2 = self.klondike.stack.get_top_cards(1)[0]
        self.assertEqual(first_card1, first_card2)
