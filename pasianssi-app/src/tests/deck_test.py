import unittest
from entities.deck import Deck


class TestDeck(unittest.TestCase):
    def setUp(self):
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        values = range(1, 14)
        self.deck = Deck(suits,values)

    def test_luodussa_pakassa_oikea_maara_kortteja(self):
        self.assertEqual(self.deck.number_of_cards, 52)

    def test_pakasta_pystyy_jakamaan_kortteja(self):
        cards = []
        for _ in range(5):
            cards.append(self.deck.deal())
        self.assertEqual(len(cards), 5)

    def test_korttien_jakaminen_vahentaa_pakassa_olevien_korttien_maaraa(self):
        for _ in range(3):
            self.deck.deal()
        self.assertEqual(self.deck.number_of_cards, 49)

    def test_pakan_uudelleenluonti_palauttaa_pakan_alkupisteeseen(self):
        self.deck.deal()
        self.deck.shuffle()
        self.deck.build()
        self.assertEqual(self.deck.number_of_cards, 52)
        self.assertEqual(str(self.deck.cards[0]), "1 of Spades")
        self.assertEqual(str(self.deck.cards[-1]), "13 of Hearts")


# adding
# clearing
# shuffling
