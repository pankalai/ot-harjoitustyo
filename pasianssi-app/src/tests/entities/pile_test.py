import unittest
from entities.pile import Pile
from entities.card import Card


class TestPile(unittest.TestCase):
    def setUp(self):
        self.pile = Pile()
        self.card1 = Card("Hearts", 11)
        self.card2 = Card("Spades", 10)
        self.card3 = Card("Diamonds", 8)
        self.card4 = Card("Clubs", 2)
        self.pile.add(self.card1)
        self.pile.add(self.card2)
        self.pile.add(self.card3)

    def test_osaa_palauttaa_tietyn_kortin_jalkeen_lisatyt_kortit_oikeassa_jarjestyksessa(self):
        sub_cards = self.pile.get_cards_on_top_of(self.card2)
        self.assertEqual(sub_cards[0], self.card3)

    def test_kortti_joka_ei_ole_pinossa(self):
        self.assertEqual(self.pile.get_cards_on_top_of(self.card4), [])

    def test_pinon_iterointi_alimmasta_alkaen(self):
        lkm = 0
        cards = []
        for card in self.pile:
            cards.append(card)
            lkm += 1
        self.assertEqual(lkm, 3)
        self.assertEqual(cards[0], self.card1)

    def test_kortin_poisto_saa_aikaan_paallimmaisen_kortin_kaantymisen(self):
        self.assertFalse(self.card2.is_visible)
        self.pile.remove(self.card3)
        self.assertTrue(self.card2.is_visible)

    def test_kortin_poisto_ei_kaanna_korttia_jos_on_jo_nakyvissa(self):
        self.card2.flip()
        self.assertTrue(self.card2.is_visible)
        self.pile.remove(self.card3)
        self.assertTrue(self.card2.is_visible)
