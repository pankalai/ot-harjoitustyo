import pygame


class Clock:
    """Pelin kelloon liittyvistä toiminnoista vastaava luokka
    """

    def __init__(self):
        """Luokan konstruktori
        """
        self._clock = pygame.time.Clock()
        self._start_time = None

    def tick(self, fps):
        """Rajoittaa kutsujen määrän maksimissaan haluttuun lukumäärään sekunnissa

        Args:
            fps (_type_): Freimien määrä sekunnissa
        """
        self._clock.tick(fps)

    def get_ticks(self):
        """Palauttaa ajan millisekunneissa edellisestä kutsusta

        Returns:
            Aika millisekunteina
        """
        return pygame.time.get_ticks()

    def start_clock(self):
        """Tallentaa kellon käynnistysajan
        """
        self._start_time = self.get_ticks()

    def elapsed_time(self):
        """Palauttaa kellon käynnistyksestä kuluneen ajan

        Returns:
            Merkkijono, jossa aika tunteina, minuutteina ja sekunteina
        """
        time_ms = self.get_ticks() - self._start_time
        spent_time = (time_ms//(1000*60*60)) % 24, (time_ms //
                                                    (1000*60)) % 60, (time_ms//1000) % 60
        return f"{spent_time[0]:02d}:{spent_time[1]:02d}:{spent_time[2]:02d}"
