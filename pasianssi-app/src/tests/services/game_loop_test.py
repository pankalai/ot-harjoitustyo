import unittest
from unittest.mock import Mock, ANY
from services.game_loop import GameLoop
from entities.card import Card
from entities.card_group import CardGroup
import pygame

pygame.init()
card = Card("Spades", 10)


class StubClock:
    def __init__(self, ticks=0):
        self.time = "00:00:00"
        self.ticks = ticks

    def get_ticks(self):
        return self.ticks

    def elapsed_time(self):
        pass

    def get_start_time(self):
        return self.time

    def start_clock(self):
        self.time = "11:11:11"


class StubEvent:
    def __init__(self, event_type, button, pos, rel=(5, 5)):
        self.type = event_type
        self.button = button
        self.pos = pos
        self.rel = rel


class StubEventQueue:
    def __init__(self, events):
        self._events = events

    def get(self):
        return self._events


class StubGame:
    def prepare(self):
        pass

    def draw(self):
        pass

    def double_click_action(self, card):
        return True

    def game_won(self):
        return False

    def deal(self):
        pass

    def create_movable_card_set(self, card):
        return [card]

    def add_to_group(self, cards, group=None):
        return True


stub_game = StubGame()


class StubRenderer:
    def __init__(self, game=stub_game):
        self.game = game

    def render(self):
        pass

    def set_cards_size(self):
        pass

    def initialize(self):
        pass

    def update_infobar(self, time, moves):
        pass

    def collide_stack(self, pos: tuple):
        return pos == (0, 0)

    def handle_stack_click(self):
        pass

    def get_top_card_at_position(self, pos):
        return card if pos == (1, 1) else None

    def handle_grabbed_cards(self, cards):
        pass

    def finish_card_move(self, card):
        pass

    def move_cards(self, cards, rel):
        pass

    def collided_groups(self, card):
        return [CardGroup()]


class TestGameLoop(unittest.TestCase):
    def setUp(self):
        self.quit_event = StubEvent(pygame.QUIT, 1, (0, 0))
        self.game_mock = Mock(wraps=stub_game)
        self.renderer_mock = Mock(wraps=StubRenderer())

    def test_palauttaa_pelin_aloittamisajan(self):
        events = [self.quit_event]
        game_loop = GameLoop(
            self.game_mock,
            self.renderer_mock,
            StubEventQueue(events),
            StubClock()
        )
        self.assertEqual(game_loop.get_start_time(), "00:00:00")
        game_loop.start(True)
        self.assertEqual(game_loop.get_start_time(), "11:11:11")

    def test_pakan_klikkaus(self):
        events = [StubEvent(pygame.MOUSEBUTTONDOWN, 1,
                            (0, 0)), self.quit_event]
        game_loop = GameLoop(
            self.game_mock,
            self.renderer_mock,
            StubEventQueue(events),
            StubClock()
        )
        game_loop.start(True)
        self.renderer_mock.collide_stack.assert_called()
        self.game_mock.deal.assert_called()

    def test_muu_kuin_pakan_klikkaus(self):
        events = [StubEvent(pygame.MOUSEBUTTONDOWN, 1,
                            (1, 1)), self.quit_event]

        game_loop = GameLoop(
            self.game_mock,
            self.renderer_mock,
            StubEventQueue(events),
            StubClock()
        )
        game_loop.start(True)
        self.renderer_mock.get_top_card_at_position.assert_called_with((1, 1))
        self.game_mock.create_movable_card_set.assert_called_with(card)
        self.renderer_mock.handle_grabbed_cards.assert_called_with([card])

    def test_tuplaklikkaus_kortti(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONUP, 1, (1, 1)),
            self.quit_event]

        game_loop = GameLoop(
            self.game_mock,
            self.renderer_mock,
            StubEventQueue(events),
            StubClock()
        )
        game_loop.start(True)
        self.renderer_mock.get_top_card_at_position.assert_called_with((1, 1))
        self.renderer_mock.finish_card_move.assert_called_with([card])
        self.assertEqual(game_loop.get_moves(), 1)

    def test_tuplaklikkaus_ei_korttia(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONUP, 1, (2, 1)),
            self.quit_event]

        game_loop = GameLoop(
            self.game_mock,
            self.renderer_mock,
            StubEventQueue(events),
            StubClock()
        )
        game_loop.start(True)
        self.renderer_mock.get_top_card_at_position.assert_called_with((2, 1))
        self.assertEqual(game_loop.get_moves(), 0)

    def test_kortin_raahaus(self):
        events = [
            StubEvent(pygame.MOUSEBUTTONDOWN, 1, (1, 1)),
            StubEvent(pygame.MOUSEMOTION, 0, (1, 1), (5, 5)),
            StubEvent(pygame.MOUSEBUTTONUP, 1, (1, 1)),
            self.quit_event]

        game_loop = GameLoop(
            self.game_mock,
            self.renderer_mock,
            StubEventQueue(events),
            StubClock(1000)
        )
        game_loop.start(True)
        self.renderer_mock.get_top_card_at_position.assert_called_with((1, 1))
        self.renderer_mock.move_cards.assert_called_with(ANY, (5, 5))
        self.renderer_mock.collided_groups.assert_called()
        self.renderer_mock.finish_card_move.assert_called()
        self.assertEqual(game_loop.get_moves(), 1)
