import unittest
from datetime import datetime
from services.clock import Clock, time_diff_in_hours_minutes_seconds, string_to_datetime


class TestClock(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.dt1 = datetime(2024, 5, 9, 11, 20, 9)
        self.dt2 = datetime(2024, 5, 9, 12, 10, 9)

    def test_palauttaa_kahden_ajan_eron(self):
        self.assertEqual(time_diff_in_hours_minutes_seconds(
            self.dt1, self.dt2), "0:50:00")

    def test_muuttaa_tekstin_ajaksi(self):
        aika_tekstina = "2024-05-09 11:20:09"
        aika = string_to_datetime(aika_tekstina)
        self.assertEqual(aika.year, 2024)
        self.assertEqual(aika.month, 5)
        self.assertEqual(aika.day, 9)
        self.assertEqual(aika.hour, 11)
        self.assertEqual(aika.minute, 20)
        self.assertEqual(aika.second, 9)

    def test_palauttaa_aloitusajan(self):
        aika = self.clock.start_clock()
        self.assertEqual(self.clock.get_start_time(), aika)
