import unittest
from services.group_handler import GroupHandler
from entities.card import Card
from entities.card_group import CardGroup

class TestGroupHandler(unittest.TestCase):
    def setUp(self):
        self.group_handler = GroupHandler()
        self.card = Card("Spades",2)
        self.card2 = Card("Spades",4)
        self.card3 = Card("Spades",7)
        self.card_group = CardGroup()
        self.card_group2 = CardGroup()
        self.group_handler.add_to_group(self.card,self.card_group)
        self.group_handler.add_to_group(self.card2,self.card_group2)

    def test_palauttaa_kortin_ryhman(self):
        self.assertEqual(self.group_handler.get_current_group(self.card),self.card_group)

    def test_jos_korttia_ei_loydy_palauttaa_none(self):
        self.assertEqual(self.group_handler.get_current_group(self.card3),None)

    def test_tyhjentaa_kaikki_ryhmat(self):
        self.assertEqual(self.card_group.number_of_cards,1)
        self.assertEqual(self.card_group2.number_of_cards,1)
        self.group_handler.clear_groups()
        self.assertEqual(self.card_group.number_of_cards,0)
        self.assertEqual(self.card_group2.number_of_cards,0)