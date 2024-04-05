import unittest
from entities.card import Card 

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card("Spades", 5)
    
    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.card, None)

    def test_kortin_maa_arvo_ja_vari_oikein(self):
        self.assertEqual(self.card.suit, "Spades")
        self.assertEqual(self.card.value, 5)
        self.assertEqual(self.card.color, "black")

    def test_kortti_merkkijonona(self):
        self.assertEqual(str(self.card), "5 of Spades")
