import unittest
from entities.pile import Pile
from entities.card import Card


class TestPile(unittest.TestCase):
    def setUp(self):
        self.pile = Pile()

    def test_osaa_palauttaa_tietyn_kortin_jalkeen_lisatyt_kortit_oikeassa_jarjestyksessa(self):
        card1 = Card("Hearts", 11)
        card2 = Card("Spades", 10)
        card3 = Card("Diamonds", 8)
        card4 = Card("Spades", 7)

        self.pile.add(card1)
        self.pile.add(card2)
        self.pile.add(card3)
        self.pile.add(card4)
        sub_cards = self.pile.get_sub_cards(card2)
        # self.assertEqual(len(sub_cards), 3)
        self.assertEqual(sub_cards[0], card2)
        self.assertEqual(sub_cards[1], card3)
        self.assertEqual(sub_cards[2], card4)

    def test_pinon_paivitys_kaantaa_paallimmaisen_kortin_nakyviin(self):
        card = Card("Hearts", 11)
        self.assertEqual(card.show, False)
        self.pile.add(card)
        self.pile.update()
        self.assertEqual(card.show, True)
