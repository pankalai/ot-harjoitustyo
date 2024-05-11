import unittest
from repositories.game_repository import game_repository
from services.game_service import GameService
from services.clock import Clock
from services.event_queue import EventQueue


class StubRenderer:
    def render(self):
        pass


class StubGame:
    def game_won(self):
        return True

    @property
    def name(self):
        return "peli"

    @property
    def level(self):
        return 1


class StubGameLoop:
    def __init__(self, game=StubGame(), event_queue=None, renderer=None, clock=Clock()):
        self.i = -1
        self.moves = [10, 2, 4, 2, 1]

    def get_moves(self):
        self.i += 1
        return self.moves[self.i]

    def get_start_time(self):
        return "2000-12-31 00:00:00"


class TestGameRepository(unittest.TestCase):
    def setUp(self):
        self.game_repository = game_repository
        self.game_repository.delete_all_played_games()
        self.game_repository.delete_all_games_and_levels()
        self.game_repository.delete_all_games()

    def test_luonti_ja_seuraava_id(self):
        self.game1 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(self.game1)
        self.assertEqual(self.game_repository.get_next_id(), 2)
        self.assertEqual(len(self.game_repository.get_all_played_games()), 1)

    def test_hae_id(self):
        self.game1 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(self.game1)
        self.assertTrue(self.game_repository._find_by_id(1))

    def test_paivitys(self):
        self.game1 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(self.game1)
        self.game_repository.add_played_game(self.game1)
        self.assertEqual(len(self.game_repository.get_all_played_games()), 1)

    def test_pelit(self):
        self.game1 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(self.game1)
        self.assertEqual(self.game_repository.find_by_game_name("peli"), 1)

    def test_pelien_tasot(self):
        self.game1 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(self.game1)
        self.assertEqual(self.game_repository.find_by_game_level(1, 1), 1)

    def test_parhaat_pelit_siirtojen_mukaan(self):
        self.game1 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(self.game1)
        game2 = GameService(
            StubGame(),
            "matti",
            StubGameLoop(),
            game_repository
        )
        self.game_repository.add_played_game(game2)
        self.assertEqual(self.game_repository.get_top_played_games_by_moves(
            "peli", 1)[0]["moves"], 2)
