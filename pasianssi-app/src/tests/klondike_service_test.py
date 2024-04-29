import unittest
from services.klondike_service import Klondike
from entities.card import Card


class TestKlondike(unittest.TestCase):
    def setUp(self):
        self.klondike = Klondike()
        self.klondike.set_level(3)
        self.klondike.draw()

    def test_jaon_jalkeen_pinot_taytetty(self):
        n = 1
        for pile in self.klondike.piles:
            self.assertEqual(pile.number_of_cards, n)
            n += 1

    def test_jaon_jalkeen_peruspakat_tyhjia(self):
        for foundation in self.klondike.foundations:
            self.assertEqual(foundation.number_of_cards, 0)

    def test_jaon_jalkeen_kasipakassa_24_korttia(self):
        self.assertEqual(self.klondike._stack.number_of_cards, 24)

    def test_kun_kaikki_kasipakan_kortit_kaannetty_pino_on_tyhja(self):
        for _ in range(int(self.klondike._stack.number_of_cards/self.klondike.turning_cards)):
            self.klondike.deal()

        self.assertEqual(self.klondike._stack.number_of_cards, 0)

    def test_assan_voi_lisata_tyhjaan_peruspakkaan(self):
        card = Card("Spades", 1)
        self.assertEqual(self.klondike.add_to_foundation(card, 0), True)

    def test_tyhjaan_peruspakkaan_ei_voi_lisata_muuta_kuin_assan(self):
        card = Card("Clubs", 3)
        self.assertEqual(self.klondike.add_to_foundation(card, None), False)

    def test_peruspakkaan_voi_lisata_kortin_jonka_arvo_yhta_suurempi(self):
        card1 = Card("Spades", 1)
        card2 = Card("Spades", 2)
        pile = self.klondike.foundations[0]
        self.klondike.add_to_foundation(card1, pile)
        self.assertEqual(self.klondike.add_to_foundation(card2, None), True)

    def test_pinoon_voi_lisata_kortin(self):
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

    def test_tyhjaan_pinoon_voi_lisata_vain_kuninkaan(self):
        pile1 = self.klondike.piles[0]
        pile1.cards.clear()
        pile2 = self.klondike.piles[1]
        pile2.cards.clear()
        self.assertEqual(self.klondike.add_to_pile(
            [Card("Spades", 13)], pile1), True)
        self.assertEqual(self.klondike.add_to_pile(
            [Card("Spades", 3)], pile2), False)

    def test_kasipakan_ensimmainen_kortti_pysyy_samana_jos_siirtoja_ei_tehda(self):
        first_card1 = self.klondike._stack.get_top_cards(1)[0]
        for _ in range(int(self.klondike._stack.number_of_cards/self.klondike.turning_cards)+1):
            self.klondike.deal()
        first_card2 = self.klondike._stack.get_top_cards(1)[0]
        self.assertEqual(first_card1, first_card2)
