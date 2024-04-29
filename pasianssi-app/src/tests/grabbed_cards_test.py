import unittest
from entities.grabbed_cards import GrabbedCards
from entities.card import Card


class TestPile(unittest.TestCase):
    def setUp(self):
        self.grabbed_cards = GrabbedCards()

        self.card1 = Card("Spades", 1)
        self.card2 = Card("Diamonds", 1)
        self.card1.set_image_size((0,0))
        self.card2.set_image_size((0,0))
        self.card1.set_position((0, 0))
        self.card2.set_position((10, 20))

        self.grabbed_cards.add(self.card1)
        self.grabbed_cards.add(self.card2)

    def test_palauttaa_kortit_lisaamisjarjestyksessa(self):
        self.assertEqual(self.grabbed_cards.get_list()[0], self.card1)
        self.assertEqual(self.grabbed_cards.get_list()[1], self.card2)

    def test_osaa_siirtaa_kaikkia_kortteja(self):
        self.grabbed_cards.move((20, 25))
        self.assertEqual((self.card1.rect.x, self.card1.rect.y), (20, 25))
        self.assertEqual((self.card2.rect.x, self.card2.rect.y), (30, 45))
