import pygame
from entities.card_group import CardGroup
from services.event_queue import EventQueue
from services.clock import Clock


class GameLoop:
    """Pelisilmukasta vastaava luokka.
    """

    def __init__(self, game, renderer, event_queue=EventQueue(), clock=Clock()):
        """Luokan konstruktori.

        Args:
            game: Luokka, joka sisältää pelin logiikan.
            renderer: Luokka, joka vastaa pelin tapahtumien päivittämisestä ruudulle.
            event_queue: Luokka, joka tarjoaa pelin tapahtumat.
            clock: Luokka, joka huolehtii aikaan liittyvistä toiminnoista.
        """
        self._game = game
        self._event_queue = event_queue
        self._renderer = renderer
        self._clock = clock

        self._click_time = 0
        self._moves = 0
        self._grabbed_cards = CardGroup()

    def get_start_time(self):
        """Palauttaa pelin alkamisajan

        Returns:
           Alkamisaika merkkijonona.
        """
        return self._clock.get_start_time()

    def initialize(self):
        """Tekee pelin alustamiseen liittyvät toimet.
        """
        self._game.prepare()
        self._renderer.set_cards_size()
        self._game.draw()
        self._renderer.initialize()

    def start(self, new_game: bool):
        """Käynnistää pelisilmukan.

        Args:
            new_game (bool): Tieto siitä, aloitetaanko kokonaan uusi peli.
            Ei suoriteta alustusta, jos jatketaan jo aloitettua.
        """
        if new_game:
            self.initialize()
            self._clock.start_clock()

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        while not self._game.game_won():
            if not self._handle_events():
                break
            self._renderer.update_infobar(
                self._clock.elapsed_time(), self._moves)
            self._renderer.render()
            self._clock.tick(60)

    def _handle_events(self):
        """Käsittelee pelin tapahtumat.

        Returns:
            False, jos peliä ei jatketa, ja True, jos jatketaan.
        """
        for event in self._event_queue.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._clock.get_ticks() - self._click_time < 500:
                    self._handle_double_click(event.pos)

                elif not self._grabbed_cards.is_empty():
                    self._handle_collision(self._grabbed_cards.bottom_card())

                self._grabbed_cards.clear()
                self._click_time = self._clock.get_ticks()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_sprite = None

                if self._renderer.collide_stack(event.pos):
                    self._game.deal()
                    self._renderer.handle_stack_click()
                else:
                    clicked_sprite = self._get_hovered_sprite(event.pos)

                if clicked_sprite:
                    self._create_crabbed_cards(clicked_sprite)

            elif event.type == pygame.MOUSEMOTION and not self._grabbed_cards.is_empty():
                self._handle_cards_move(event.rel)

        return True

    def _handle_double_click(self, pos: tuple):
        """Käsittelee tuplaklikkauksen.

        Args:
            pos (tuple): Sijainti, jossa tuplaklikkaus tapahtui.
        """
        clicked_sprite = self._get_hovered_sprite(pos)
        if clicked_sprite:
            if self._game.double_click_action([clicked_sprite]):
                self._moves += 1
            self._renderer.finish_card_move([clicked_sprite])

    def _create_crabbed_cards(self, card):
        """Luo siirrettävän korttiryhmän.

        Args:
            card: Card-luokan olio, jonka perusteella korttiryhmä muodostetaan.
        """
        card_list = self._game.create_movable_card_set(card)
        for item in card_list:
            self._grabbed_cards.add(item)
        self._renderer.handle_grabbed_cards(card_list)

    def _handle_cards_move(self, rel: tuple):
        """Käsittelee korttien liikuttamisen.

        Args:
            rel (tuple): Muutos suhteessa edelliseen sijaintiin pikseleinä.
        """
        self._renderer.move_cards(self._grabbed_cards.as_list(), rel)

    def _handle_collision(self, bottom_card):
        """Käsittelee korttiryhmän siirtämisen. 
        Testaa voiko kortit siirtää johonkin niistä kohteista,
        joiden kanssa annettu kortti törmää.

        Args:
            bottom_card: Siirrettävän korttiryhmän pohjimmainen kortti.
        """
        for group in self._renderer.collided_groups(bottom_card):
            if self._game.add_to_group(self._grabbed_cards.as_list(), group):
                self._moves += 1
                break
        self._renderer.finish_card_move(self._grabbed_cards.as_list())

    def _get_hovered_sprite(self, position: tuple):
        """Palauttaa päällimmäisen kortin, joka on annetussa sijainnissa.

        Args:
            position (tuple): Sijainti x- ja y-koordinaatteina.

        Returns:
            Card-luokan olio.
        """
        return self._renderer.get_top_card_at_position(position)

    def get_moves(self):
        """Palauttaa tehdyt siirrot.

        Returns:
            Siirtojen lukumäärä.
        """
        return self._moves
