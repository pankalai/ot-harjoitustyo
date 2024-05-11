import unittest
from entities.card import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card("Spades", 5)
        self.card2 = Card("Spades", 11)
        self.card3 = Card("Spades", 12)
        self.card4 = Card("Spades", 13)
        self.card5 = Card("Spade", 13)
        self.card.set_image_size((15, 45))
        self.card._set_image()

    def test_luotu_kortti_on_olemassa(self):
        self.assertIsNotNone(self.card)

    def test_kortin_maa_arvo_ja_vari_oikein(self):
        self.assertEqual(self.card.suit, "Spades")
        self.assertEqual(self.card.rank, 5)
        self.assertEqual(self.card.color, "black")
        self.assertIsNone(self.card5.color)

    def test_kortti_merkkijonona(self):
        self.assertEqual(str(self.card), "5 of Spades")

    def test_kortin_sijainti(self):
        self.card.set_position((10, 10))
        self.assertEqual(self.card.get_position(), (10, 10))

    def test_kortin_siirto(self):
        self.card.set_position((15, 10))
        self.card.move((0, 5))
        self.assertEqual(self.card.get_position(), (15, 15))

    def test_vaihtoehtoinen_arvo(self):
        self.assertEqual(self.card._alternative_rank(), 5)
        self.assertEqual(self.card2._alternative_rank(), "jack")
        self.assertEqual(self.card3._alternative_rank(), "queen")
        self.assertEqual(self.card4._alternative_rank(), "king")

    def test_kaanto_saa_aikaan_kuvan_muutoksen(self):
        image = self.card.image
        self.card.flip()
        self.card.update()
        self.assertNotEqual(self.card.image, image)
