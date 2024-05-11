import os
import pygame
from ui.element import InfoBar
from ui.ui_settings import klondike_ui_settings
from services.klondike import klondike_service


dirname = os.path.dirname(__file__)


class Renderer:
    """Näytön piirtämisestä vastaava yliluokka, joka vastaa tietopalkista.
    """

    def __init__(self, window):
        """Luokan konstruktori.

        Args:
            window: Ikkuna, johon piirretään.
        """
        self._window = window
        self._infobar = InfoBar()

    def update_infobar(self, time: str, moves: int):
        """Päivittää ajan ja siirrot tietopalkkiin.

        Args:
            time (str): Kulunut aika.
            moves (int): Tehdyt siirrot.
        """
        self._infobar.update_info(time, moves)

    def _update(self):
        """Piirtää alapalkin ja päivittää näkymän
        """
        self._infobar.draw(self._window)
        pygame.display.update()


class GameRenderer(Renderer):
    """Pelin näkymän piirtämisestä vastaava luokka.

    Args:
        Perii Renderer-luokan.
    """

    def __init__(self, window=None, game=klondike_service, ui_settings=klondike_ui_settings):
        """Luokan konstruktori.

        Args:
            window: Ikkuna, johon piirretään.
            game: Pelin logiikan sisältävä luokka.
            ui_settings: Ulkoasun asetukset.
        """
        super().__init__(window)

        self.ui_settings = ui_settings

        self._game = game

        self._stack_area = None
        self._stack_image = None
        self._stack_and_waste_area = None
        self._update_stack = True

        self._waste = pygame.sprite.LayeredUpdates()
        self._layered_cards = pygame.sprite.LayeredUpdates()
        self._rects_to_collide = pygame.sprite.Group()

    def set_cards_size(self):
        """Asettaa korttien koon
        """
        for card in self._game.deck:
            card.set_image_size(self.ui_settings.card_size)

    def initialize(self):
        """Näytön alustaminen.
        """
        self._create_rects()
        self._initialize_cards_positions()

        # Stack image
        image = pygame.image.load(
            os.path.join(dirname, "..", r"assets/cards", "back-side.png")
        )
        self._stack_image = pygame.transform.smoothscale(
            image, self.ui_settings.card_size)

        self._stack_area = pygame.Rect(
            self.ui_settings.stack_position, self.ui_settings.card_size)

        width = (self.ui_settings.waste_position[0]-self.ui_settings.stack_position[0]
                 )+3*self.ui_settings.waste_offset+self.ui_settings.card_size[0]
        self._stack_and_waste_area = pygame.Rect(
            self.ui_settings.stack_position, (width, self.ui_settings.card_size[1]))

    def _create_rects(self):
        """Luo alueet, joihin kortteja on mahdollista siirtää.
        """
        # Foundations
        left_pos, top_pos = self.ui_settings.foundation_position
        for foundation in self._game.foundations:
            foundation.set_rect((left_pos, top_pos),
                                self.ui_settings.card_size)
            left_pos += self.ui_settings.foundation_offset

            self._rects_to_collide.add(foundation)

        # Piles
        # The height of pile is set to the bottom of the window
        left_pos, top_pos = self.ui_settings.pile_position
        for pile in self._game.piles:
            pile.set_rect(
                (left_pos, top_pos),
                (self.ui_settings.card_size[0],
                 self._window.get_height()-top_pos)
            )
            left_pos += self.ui_settings.pile_offset_left

            self._rects_to_collide.add(pile)

    def _initialize_cards_positions(self):
        """Asettaa korttien sijainnit pelin alussa.
        """
        left_pos = self.ui_settings.pile_position[0]
        for pile in self._game.piles:
            top_pos = self.ui_settings.pile_position[1]
            for card in pile:
                card.set_position((left_pos, top_pos))
                top_pos += self.ui_settings.pile_offset_top
                self._layered_cards.add(card)
            left_pos += self.ui_settings.pile_offset_left

    def _update_card_position(self, card, group=None):
        """Päivittää kortin sijainnin.

        Args:
            card: Card-luokan olio, jonka sijainti päivitetään.
        """
        if not group:
            group = self._game.get_card_group(card)

        if group in self._game.piles:
            group_index = self._game.piles.index(group)
            card_index = self._game.get_card_index_in_group(card, group)
            card.set_position(
                (self.ui_settings.pile_position[0]+group_index*self.ui_settings.pile_offset_left,
                 self.ui_settings.pile_position[1]+card_index*self.ui_settings.pile_offset_top)
            )
        elif group in self._game.foundations:
            index = self._game.foundations.index(group)
            left_pos, top_pos = self.ui_settings.foundation_position
            card.set_position(
                (left_pos+index*self.ui_settings.foundation_offset, top_pos))

    def collide_stack(self, pos: tuple):
        """Palauttaa tiedon, törmääkö annettu sijainti käsipakan kanssa.

        Args:
            pos (tuple): Sijainti x- ja y-koordinaatteina.

        Returns:
           True, jos törmää, muuten False.
        """
        return self._stack_area.collidepoint(pos)

    def handle_stack_click(self):
        """Käsittelee käsipakan klikkaamisen.
        """
        self._update_stack = True

    def handle_grabbed_cards(self, card_list: list):
        """Käsittelee siirrettävät kortit.
        Tuo kortit kaikkiin kortteihin nähden päällimmäisiksi.

        Args:
            card_list (list): Siirrettävät kortit.
        """
        for card in card_list:
            if card not in self._layered_cards:
                self._layered_cards.add(card)
            self._layered_cards.move_to_front(card)

    def move_cards(self, card_list: list, rel: tuple):
        """Siirtää kortteja.

        Args:
            card_list (list): Siirrettävät kortit listana.
            rel (tuple): Sijainnin suhteellinen muutos.
        """
        for card in card_list:
            card.move(rel)

    def finish_card_move(self, card_list: list):
        """Korttien toteutuneeseen siirtoon liittyvät toimenpiteet, kuten 
        poistaminen kerroksittaisesta korttiryhmästä, jos siirto ei toteutunut,
        ja sijainnin päivitys.

        Args:
            card_list (list): Siirretyt kortit.
        """
        group = self._game.get_card_group(card_list[0])
        if group not in self._game.piles + self._game.foundations:
            self._layered_cards.remove(card_list)
        for card in card_list:
            self._update_card_position(card, group)
        self._update_stack = True

    def collided_groups(self, card):
        """Ryhmät, joihin annettu kortti törmää.

        Args:
            card: Kortti, jonka törmääminen tutkitaan.

        Returns:
            Listana ryhmät, joihin kortti törmää.
        """
        groups = []
        for group in self._rects_to_collide:
            if pygame.sprite.collide_rect(card, group):
                groups.append(group)
        return groups

    def get_top_card_at_position(self, position: tuple):
        """Palauttaa päällimmäisen kortin annetussa sijainnissa.

        Args:
            position (tuple): Sijainti x- ja y-koordinaatteina.

        Returns:
           Kortti, joka on annetussa sijainnissa.
        """
        card_list = self._layered_cards.get_sprites_at(position)
        if not card_list:
            card_list = self._waste.get_sprites_at(position)
        if card_list:
            return card_list[-1]
        return None

    def _create_waste(self):
        """Luo käsipakasta käännetyt kortit.
        """
        self._waste.empty()
        for i, card in enumerate(self._game.get_waste_top_cards()):
            self._waste.add(card)
            card.set_position(
                (self.ui_settings.waste_position[0]+i*self.ui_settings.waste_offset,
                 self.ui_settings.waste_position[1])
            )
            self._waste.move_to_front(card)

    def _draw_stack(self):
        """Piirtää käsipakan. Jos käsipakassa on kortteja jäljellä, 
        niin piirretään kuvapuoli alaspäin oleva kortti. Muussa tapauksessa
        piirretään suorakulmio merkitsemään käsipakan paikkaa.
        """
        if self._game.stack_is_empty():
            pygame.draw.rect(self._window, self.ui_settings.empty_stack_color,
                             (self.ui_settings.stack_position, self.ui_settings.card_size), 1)
        else:
            self._window.blit(self._stack_image, self._stack_area)

    def _draw_foundations(self):
        """Piirtää peruspakoissa olevat kortit.
        """
        for i, foundation in enumerate(self._game.foundations):
            if foundation.is_empty():
                pygame.draw.rect(
                    self._window,
                    self.ui_settings.empty_foundation_color,
                    ((self.ui_settings.foundation_position[0]+i*self.ui_settings.foundation_offset,
                      self.ui_settings.foundation_position[1]),
                     self.ui_settings.card_size),
                    1
                )

    def render(self):
        """Piirtää näkymän.
        """
        self._window.fill(self.ui_settings.background_color)

        self._draw_stack()
        self._draw_foundations()

        if self._update_stack:
            self._create_waste()
            self._update_stack = False

        self._waste.update()
        self._waste.draw(self._window)

        self._layered_cards.update()
        self._layered_cards.draw(self._window)

        self._update()
