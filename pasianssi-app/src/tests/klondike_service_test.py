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
            self.assertEqual(len(pile), n)
            n += 1

    def test_after_draw_foundations_are_empty(self):
        for foundation in self.klondike.foundations:
            self.assertEqual(len(foundation), 0)

    def test_after_draw_stock_includes_24_cards(self):
        self.assertEqual(len(self.klondike.stack), 24)

    def test_after_all_cards_are_dealt_stock_is_empty_and_waste_full(self):
        for _ in range(int(len(self.klondike.stack)/self.klondike.turning_cards)):
            self.klondike.deal()

        self.assertEqual(len(self.klondike.stack), 0)

    def test_can_add_ace_to_empty_foundation(self):
        card = Card("Spades", 1)
        self.assertEqual(self.klondike.add_to_foundation(card, 0), True)

    def test_can_add_valid_card_on_foundation(self):
        card1 = Card("Spades", 1)
        card2 = Card("Spades", 2)
        card3 = Card("Clubs", 3)
        self.assertEqual(self.klondike.add_to_foundation(card1, None), True)
        self.assertEqual(self.klondike.add_to_foundation(card2, None), True)
        self.assertEqual(self.klondike.add_to_foundation(card3, None), False)

    def test_can_add_valid_card_on_pile(self):
        cards = []
        i = 0
        while True:
            if self.klondike.piles[i][-1].rank != 1:
                rank = self.klondike.piles[i][-1].rank-1
                if self.klondike.piles[i][-1].suit in ("Diamonds", "Hearts"):
                    suit = "Spades"
                else:
                    suit = "Diamonds"
                break
            i += 1
        cards.append(Card(suit, rank))
        self.assertEqual(self.klondike.add_to_pile(cards, i), True)
        self.assertEqual(self.klondike.add_to_pile(cards, i), False)

    def test_can_add_only_king_on_empty_pile(self):
        self.klondike.piles[0] = []
        self.klondike.piles[1] = []
        self.assertEqual(self.klondike.add_to_pile(
            [Card("Spades", 13)], 0), True)
        self.assertEqual(self.klondike.add_to_pile(
            [Card("Spades", 3)], 1), False)
