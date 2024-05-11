from datetime import datetime
import pygame


class Clock:
    """Pelin kelloon liittyvistä toiminnoista vastaava luokka.
    """

    def __init__(self):
        """Luokan konstruktori.
        """
        self._clock = pygame.time.Clock()
        self._start_time = None
        self._start_time_in_ticks = None

    def tick(self, fps):
        """Rajoittaa kutsujen määrän maksimissaan haluttuun lukumäärään sekunnissa.

        Args:
            Freimien määrä sekunnissa.
        """
        self._clock.tick(fps)

    def get_ticks(self):
        """Palauttaa pygamen alustuksesta kuluneen ajan.

        Returns:
            Aika millisekunteina.
        """
        return pygame.time.get_ticks()

    def start_clock(self):
        """Tallentaa kellon käynnistysajan.
        """
        self._start_time_in_ticks = self.get_ticks()
        self._start_time = get_current_time()
        return self._start_time

    def get_start_time(self):
        """Palauttaa käynnistysajan

        Returns:
            Datetime merkkijonona.
        """
        return self._start_time

    def elapsed_time(self):
        """Palauttaa kellon käynnistyksestä kuluneen ajan.

        Returns:
            Merkkijono, jossa aika tunteina, minuutteina ja sekunteina.
        """
        time_ms = self.get_ticks() - self._start_time_in_ticks
        spent_time = (time_ms//(1000*60*60)) % 24, (time_ms //
                                                    (1000*60)) % 60, (time_ms//1000) % 60
        return f"{spent_time[0]:02d}:{spent_time[1]:02d}:{spent_time[2]:02d}"


def get_current_time():
    """Palauttaa tämänhetkisen ajan.

    Returns:
        Aika merkkijonona.
    """
    return datetime_to_string(datetime.now())


def datetime_to_string(time):
    """Muuttaa ajan merkkijonoksi

    Args:
        Aika datetime-tyyppinä.

    Returns:
        Aika merkkijonona: Vuosi-Kuukausi-Päivä Tunti:Minuutti:Sekunti.
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


def string_to_datetime(string):
    """Muuttaa merkkijonon datetime-tyypiksi.

    Args:
        Aika merkkijonona.

    Returns:
       Aika datetime-tyyppinä.
    """
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def time_diff_in_hours_minutes_seconds(datetime1, datetime2):
    """Palauttaa kahden ajan erotuksen tunteina, minuutteina ja sekunteina.

    Args:
        datetime1: Ensimmäinen aika.
        datetime2: Toinen aika.

    Returns:
        Erotus merkkijonona.
    """
    dt1 = datetime.timestamp(datetime1)
    dt2 = datetime.timestamp(datetime2)

    dt1 = datetime.fromtimestamp(dt1)
    dt2 = datetime.fromtimestamp(dt2)

    return str(dt2 - dt1)
