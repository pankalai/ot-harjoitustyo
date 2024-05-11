import unittest
from entities.card_group import CardGroup
from entities.card import Card


class TestCardGroup(unittest.TestCase):
    def setUp(self):
        self.card_group = CardGroup()
        self.card = Card("Hearts", 11)

    def test_palauttaa_kortit_listana(self):
        self.assertEqual(self.card_group.as_list(), [])
        self.card_group.add(self.card)
        self.assertEqual(self.card_group.as_list(), [self.card])

    def test_palauttaa_pohjimmaisen_kortin(self):
        self.assertIsNone(self.card_group.bottom_card())
        self.card_group.add(self.card)
        self.assertEqual(self.card_group.bottom_card(), self.card)

    def test_poistaa_kortin_ryhmasta(self):
        self.assertIsNone(self.card_group.remove(self.card))
