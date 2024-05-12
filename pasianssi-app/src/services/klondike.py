from entities.deck import Deck
from entities.card import Card
from entities.card_group import CardGroup
from entities.pile import Pile
from services.group_handler import GroupHandler


class Klondike:
    """Klondike-pasianssin logiikasta vastaava luokka.
    """

    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
    ranks = range(1, 14)

    def __init__(self, level=3, group_handler=GroupHandler()):
        """Luokan konstruktori.

        Args:
            level (int, optional): Pelin vaikeustaso.
            group_handler: Korttien siirtelystä vastaava olio, 
            oletuksena GroupHandler().
        """
        self.deck = Deck(Klondike.suits, Klondike.ranks)

        self.piles = [Pile() for _ in range(7)]
        self.foundations = [CardGroup() for _ in range(4)]
        self._stack = CardGroup()
        self._waste = CardGroup()

        self.set_level(level)
        self._group_handler = group_handler

    @property
    def name(self):
        """Palauttaa pelin nimen

        Returns:
            Nimi merkkijonona.
        """
        return "Klondike"

    @property
    def level(self):
        """Palauttaa pelin vaikeustason.

        Returns:
            Vaikeustaso kokonaislukuna.
        """
        return self._level

    @property
    def double_click_action(self):
        """Palauttaa tiedon siitä, mikä metodi liittyy tuplaklikkaus-tapahtumaan.

        Returns:
            Luokan metodi.
        """
        return self.add_to_group

    def set_level(self, level: int):
        """Pelin vaikeustason asettaminen.

        Args:
            level (int): Käsipakasta kerralla käännettävien korttien määrä.
        """
        self._level = level

        if level == 1:
            self._turning_cards = 1
        elif level == 3:
            self._turning_cards = 3

        return self

    def prepare(self):
        """Valmistelee pelin luomalla pakan ja sekoittamalla sitä
        sekä tyhjentämällä eri korttiryhmät.
        """
        self.deck.build()
        self.deck.shuffle()
        self._group_handler.clear_card_groups()
        self._group_handler.clear_groups()

    def draw(self):
        """Jakaa kortit pinoihin ja asettaa loput kortit käsipakkaan.
        """
        pile_n = 1
        for pile in self.piles:
            for i in range(pile_n):
                card = self.deck.deal()
                self._group_handler.add_to_group(card, pile)
                if i == pile_n-1:
                    card.flip()
            pile_n += 1

        for card in self.deck:
            self._group_handler.add_to_group(card, self._stack)

        self._stack.reverse()

    def deal(self):
        """Korttien kääntäminen käsipakasta.
        """
        if not self._stack.is_empty():
            for _ in range(min(self._turning_cards, self._stack.number_of_cards)):
                card = self._stack.get_top_cards(1)[0]
                self._group_handler.add_to_group(card, self._waste)
                card.flip()
        else:
            for card in self._waste:
                self._group_handler.add_to_group(card, self._stack)
                card.flip()

    def _add_to_pile(self, card_list: list, pile: Pile):
        """Lisää yhden tai useamman kortin pinoon, jos se on sallittua.

        Args:
            card_list (list): Card-luokan olio.
            pile (Pile): Pile-luokan olio.

        Returns:
            True, jos siirto on sallittu.
        """
        if pile in self.piles:
            if valid_to_pile(card_list[0], pile):
                for card in card_list:
                    self._group_handler.add_to_group(card, pile)
                return True
        return False

    def _add_to_foundation(self, card, foundation=None):
        """Lisää kortin peruspakkaan. Jos peruspakkaa ei ole määritelty,
        käy läpi kaikki peruspakat.

        Args:
            card: Card-luokan olio tai lista, joka sisältää Card-luokan olion.
            foundation: Peruspakka, johon kortti lisätään.

        Returns:
            True, jos kortti voidaan siirtää peruspakkaan.
        """
        if isinstance(card, list):
            if len(card) > 1:
                return False
            card = card[0]

        if foundation:
            if foundation in self.foundations:
                if valid_to_foundation(card, foundation):
                    self._group_handler.add_to_group(card, foundation)
                    return True
        else:
            for fnd in self.foundations:
                if valid_to_foundation(card, fnd):
                    self._group_handler.add_to_group(card, fnd)
                    return True

        return False

    def get_card_group(self, card: Card):
        """Palauttaa ryhmän, jossa kortti sillä hetkellä on.

        Args:
            card (Card): kortti, jonka ryhmä haetaan.

        Returns:
            Ryhmän olio, jossa kortti on.
        """
        return self._group_handler.get_current_group(card)

    def get_card_index_in_group(self, card: Card, group=None):
        """Palauttaa kortin sijainnin ryhmässään.

        Args:
            card (Card): Kortti, jota haetaan.
            group: Kortin ryhmä. Jos tieto puuttuu, ryhmä
            selvitetään ryhmäkäsittelijältä.

        Returns:
            Kortin indeksi ryhmässä.
        """
        if not group:
            group = self.get_card_group(card)

        return group.card_index(card)

    def get_waste_top_cards(self):
        """Palauttaa kolme päällimmäistä käsipakasta käännettyä korttia.

        Returns:
            Lista kortteja.
        """
        return self._waste.get_top_cards(3)

    def _get_cards_on_top_of(self, card: Card):
        """Palauttaa tietyn kortin päällä olevat kortit.

        Args:
            card (Card): Kortti, jonka päällä olevat kortit haetaan. Card-luokan olio.

        Returns:
            Lista kortteja. Jos kortti ei ole missään pinossa, niin tyhjä lista.
        """
        group = self._group_handler.get_current_group(card)
        if group in self.piles:
            return group.get_cards_on_top_of(card)
        return []

    def stack_is_empty(self):
        """Palauttaa tiedon, onko käsipakka tyhjä.

        Returns:
            True, jos käsipakassa ei ole kortteja eli joko kaikki on käännetty tai pelattu pöytään.
        """
        return self._stack.is_empty()

    def game_won(self):
        """Onko peli päättynyt eli onko jokaisessa peruspakassa 13 korttia.

        Returns:
            True, jos kaikki kortit ovat peruspakoissa.
        """
        return not (False in [group.number_of_cards == 13 for group in self.foundations])

    def _is_movable(self, card: Card):
        """Palauttaa tiedon, onko kortti mahdollista siirtää.

        Args:
            card (Card): Kortti, jota ollaan siirtämässä.

        Returns:
            True, jos kortti on siirrettävissä, muuten False.
        """
        if not card.is_visible:
            return False
        group = self._group_handler.get_current_group(card)
        return group.get_top_cards(1)[0] == card or (group in self.piles)

    def create_movable_card_set(self, card: Card):
        """Luo siirrettävän korttiryhmän.

        Args:
            card (Card): Kortti, jonka perusteella ryhmä luodaan.

        Returns:
            Lista kortteja.
        """
        if not self._is_movable(card):
            return []
        return [card] + self._get_cards_on_top_of(card)

    def add_to_group(self, card_group: list, group=None):
        """Lisää kortit ryhmään, jos se on sallittua. 

        Args:
            card_group (list): Lista kortteja, joita ollaan lisäämässä.
            group: Ryhmä, johon ollaan lisäämässä. Jos puuttuu, niin
            tulkitaan, että ollaan siirtämässä peruspakkaan.

        Returns:
            True, jos siirto on mahdollinen, muuten False.
        """
        if not self._is_movable(card_group[0]):
            return False

        current_group = self.get_card_group(card_group[0])
        if not group and current_group.get_top_cards(1)[0] != card_group[0]:
            return False

        if group in self.piles:
            return self._add_to_pile(card_group, group)

        if not group or group in self.foundations:
            return self._add_to_foundation(card_group, group)

        return False


def valid_to_pile(card: Card, pile: Pile):
    """Onko kortti kelvollinen pinoon.

    Args:
        card (Card): Kortti, jota ollaan siirtämässä. Card-luokan olio.
        pile (Pile): Pino, johon ollaan siirtämässä. Pile-luokan olio.

    Returns:
        True, jos kortti on kelvollinen pinoon.
    """
    if pile.is_empty():
        return card.rank == 13

    top_card = pile.get_top_cards(1)[0]
    if top_card.color != card.color and top_card.rank == card.rank+1:
        return True
    return False


def valid_to_foundation(card: Card, foundation: CardGroup):
    """Onko kortti kelvollinen peruspakkaan.

    Args:
        card (Card): Kortti, jota ollaan siirtämässä. Card-luokan olio.
        foundation (CardGroup): Peruspakka, johon ollaan siirtämässä. CardGroup-luokan olio.

    Returns:
        True, jos kortti on kelvollinen peruspakkaan.
    """
    if foundation.is_empty():
        return card.rank == 1

    top_card = foundation.get_top_cards(1)[0]
    return top_card.suit == card.suit and top_card.rank == card.rank-1


klondike_service = Klondike()
