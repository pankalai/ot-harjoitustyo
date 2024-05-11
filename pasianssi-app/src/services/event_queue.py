import pygame


class EventQueue:
    """Pygamen tapahtumajono.
    """

    def get(self):
        """Palauttaa pygamen tapahtumajonon.

        Returns:
           Tapahtumat listana.
        """
        return pygame.event.get()


event_queue = EventQueue()
