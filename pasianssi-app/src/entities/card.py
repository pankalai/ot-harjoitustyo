import os
import pygame

dirname = os.path.dirname(__file__)

class Card(pygame.sprite.Sprite):
    def __init__(self, suit, rank, show = False, size = (0,0)):
        super().__init__()

        self.suit = suit
        self.rank = rank
        self.show = show

        if self.suit in ("Diamonds", "Hearts"):
            self.color = "red"
        elif self.suit in ("Spades", "Clubs"):
            self.color = "black"
        else:
            self.color = None

        self.size = size
        self.set_image()

        self.rect = None

    def flip(self):
        self.show = not self.show

    def set_image_size(self, size):
        self.size = size
        self.set_image()

    def set_position(self, position):
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def set_image(self):
        if self.show:
            image = pygame.image.load(
                os.path.join(dirname, "..", r"assets\cards",
                             self.filename + ".png")
            )
            self.front_side_image = True
        else:
            image = pygame.image.load(
                os.path.join(dirname, "..", r"assets\cards", "back-side.png")
            )
            self.front_side_image = False

        self.image = pygame.transform.scale(image, self.size)

    @property
    def alternative_rank(self):
        if self.rank == 1:
            file_rank = "ace"
        elif self.rank == 11:
            file_rank = "jack"
        elif self.rank == 12:
            file_rank = "queen"
        elif self.rank == 13:
            file_rank = "king"
        else:
            file_rank = self.rank
        return file_rank

    @property
    def filename(self):
        return f"{self.alternative_rank}_of_{self.suit.lower()}"

    def update(self):
        if self.show != self.front_side_image:
            self.set_image()

    def __str__(self):
        return f"{self.rank} of {self.suit}"
