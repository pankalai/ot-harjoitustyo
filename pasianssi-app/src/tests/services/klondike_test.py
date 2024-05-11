import unittest
from services.klondike import Klondike
from entities.card import Card
from entities.pile import Pile
from entities.card_group import CardGroup


class TestKlondike(unittest.TestCase):
    def setUp(self):
        self.klondike = Klondike()
        self.klondike.set_level(3)
        self.klondike.draw()
        self.card1 = Card("Spades", 1)
        self.card2 = Card("Clubs", 3)
        self.card3 = Card("Spades", 13)

    def test_palauttaa_pelin_nimen_ja_tason(self):
        self.assertEqual(self.klondike.name, "Klondike")
        self.klondike.set_level(3)
        self.assertEqual(self.klondike.level, 3)
        self.klondike.set_level(1)
        self.assertEqual(self.klondike.level, 1)

    def test_valmistelu_tyhjentaa_ryhmat(self):
        pile = Pile()
        self.klondike._group_handler.add_to_group(self.card1, pile)
        self.assertEqual(pile.number_of_cards, 1)
        self.klondike.prepare()
        self.assertEqual(pile.number_of_cards, 0)

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
        self.assertFalse(self.klondike.stack_is_empty())
        for _ in range(int(self.klondike._stack.number_of_cards/self.klondike._turning_cards)):
            self.klondike.deal()

        self.assertEqual(self.klondike._stack.number_of_cards, 0)
        self.assertTrue(self.klondike.stack_is_empty())

    def test_assan_voi_lisata_tyhjaan_peruspakkaan(self):
        self.assertTrue(self.klondike._add_to_foundation(self.card1, 0))

    def test_tyhjaan_peruspakkaan_ei_voi_lisata_muuta_kuin_assan(self):
        self.assertFalse(self.klondike._add_to_foundation(self.card2, None))

    def test_peruspakkaan_voi_lisata_kortin_jonka_arvo_yhta_suurempi(self):
        card2 = Card("Spades", 2)
        pile = self.klondike.foundations[0]
        self.klondike._add_to_foundation(self.card1, pile)
        self.assertTrue(self.klondike._add_to_foundation(card2, None))

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
        self.assertTrue(self.klondike._add_to_pile(
            cards, self.klondike.piles[i]))
        self.assertFalse(self.klondike._add_to_pile(
            cards, self.klondike.piles[i]))

    def test_tyhjaan_pinoon_voi_lisata_vain_kuninkaan(self):
        pile1 = self.klondike.piles[0]
        pile1.clear()
        pile2 = self.klondike.piles[1]
        pile2.clear()
        self.assertTrue(self.klondike._add_to_pile(
            [self.card3], pile1))
        self.assertFalse(self.klondike._add_to_pile(
            [self.card1], pile2))

    def test_kasipakan_ensimmainen_kortti_pysyy_samana_jos_siirtoja_ei_tehda(self):
        first_card1 = self.klondike._stack.get_top_cards(1)[0]
        for _ in range(int(self.klondike._stack.number_of_cards/self.klondike._turning_cards)+1):
            self.klondike.deal()
        first_card2 = self.klondike._stack.get_top_cards(1)[0]
        self.assertEqual(first_card1, first_card2)

    def test_peruspakkaan_lisays_kun_kortit_listassa(self):
        foundation1 = self.klondike.foundations[0]
        foundation2 = CardGroup()
        self.assertFalse(self.klondike._add_to_foundation(
            [self.card1, self.card2], foundation1))
        self.assertFalse(self.klondike._add_to_foundation(
            [self.card2], foundation1))
        self.assertTrue(self.klondike._add_to_foundation(
            [self.card1], foundation1))
        self.assertFalse(self.klondike._add_to_foundation(
            [self.card1], foundation2))

    def test_palauttaa_kortin_ryhman(self):
        foundation1 = self.klondike.foundations[0]
        self.klondike._add_to_foundation([self.card1], foundation1)
        self.assertEqual(self.klondike.get_card_group(self.card1), foundation1)

    def test_palauttaa_kortin_indeksin_ryhmassa(self):
        foundation1 = self.klondike.foundations[0]
        self.klondike._add_to_foundation([self.card1], foundation1)
        self.assertEqual(self.klondike.get_card_index_in_group(
            self.card1, foundation1), 0)
        self.assertEqual(self.klondike.get_card_index_in_group(self.card1), 0)

    def test_palauttaa_kortin_paalla_olevat_kortit(self):
        card1 = self.klondike.piles[1].bottom_card()
        card2 = self.klondike.piles[1].get_top_cards(1)[0]
        self.assertEqual(self.klondike._get_cards_on_top_of(card1), [card2])
        card2 = self.klondike._stack._cards[-2]
        self.assertEqual(self.klondike._get_cards_on_top_of(card2), [])

    def test_palauttaa_tiedon_onko_peli_mennyt_lapi(self):
        self.assertEqual(self.klondike.game_won(), False)

    def test_kertoo_onko_kortti_siirrettavissa(self):
        card1 = self.klondike.piles[3].bottom_card()
        card2 = self.klondike.piles[3].get_top_cards(1)[0]
        self.assertFalse(self.klondike._is_movable(card1))
        self.assertTrue(self.klondike._is_movable(card2))

    def test_luo_siirrettavien_korttien_ryhman(self):
        card3, card2, card1 = tuple(self.klondike.piles[3].get_top_cards(3))
        card2.flip()
        self.assertEqual(
            self.klondike.create_movable_card_set(card2), [card2, card1])
        self.assertEqual(self.klondike.create_movable_card_set(card3), [])

    def test_lisaa_kortin_ryhmaan(self):
        self.klondike.deal()
        card1, card2 = tuple(self.klondike.piles[3].get_top_cards(2))
        card3 = self.klondike._waste.get_top_cards(1)[0]
        pile = self.klondike.piles[0]
        foundation = self.klondike.foundations[0]
        self.assertFalse(self.klondike.add_to_group([card1]))
        self.assertFalse(self.klondike.add_to_group([self.card1], pile))
        self.assertFalse(self.klondike.add_to_group([card3], pile))
        self.assertFalse(self.klondike.add_to_group([card3], foundation))
