import os
import pygame

dirname = os.path.dirname(__file__)


class Card(pygame.sprite.Sprite):
    """Luokka, jonka avulla ylläpidetään tietoa yksittäisestä pelikortista

    Args:
        Perii pygamen sprite-luokan
    """

    def __init__(self, suit: str, rank: int, show: bool = False):
        """Luokan konstruktori, joka luo uuden pelikortin

        Args:
            suit (str): kortin maa
            rank (int): kortin arvo
            show (bool, optional): onko kortti näkyvissä eli kuvapuoli ylöspäin, 
            oletusarvona kuvapuoli on alaspäin
        """
        super().__init__()

        self.suit = suit
        self.rank = rank
        self.show = show

        self.rect = None
        self.image = None
        self.image_size = None
        self.front_side_image = None

    @property
    def color(self):
        """Palauttaa kortin värin

        Returns:
            Tavanomaisen pakan tapauksessa punainen tai musta, muutoin None
        """
        if self.suit in ("Diamonds", "Hearts"):
            return "red"
        if self.suit in ("Spades", "Clubs"):
            return "black"
        return None

    def flip(self):
        """Kääntää kortin ympäri
        """
        self.show = not self.show

    def set_image_size(self, size: tuple):
        """Asettaa kortin kuvakoon

        Args:
            size (tuple): kortin koko tuplena (leveys,korkeus)
        """
        self.image_size = size
        self.set_image()

    def set_position(self, position: tuple):
        """Asettaa kortin sijainnin

        Args:
            position (tuple): kortin sijainti tuplena (vasen,ylä)
        """
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def set_image(self):
        """Lataa kortin kuvan
        """
        if self.show:
            image = pygame.image.load(
                os.path.join(dirname, "..", r"assets/cards",
                             self.filename() + ".png")
            )
            self.front_side_image = True
        else:
            image = pygame.image.load(
                os.path.join(dirname, "..", r"assets/cards", "back-side.png")
            )
            self.front_side_image = False

        self.image = pygame.transform.smoothscale(image, self.image_size)

    def alternative_rank(self):
        """Palauttaa kuvakortin vaihtoehtoisen arvon

        Returns:
            Kortin arvo, jos kyseessä ei ole kuvakortti, muussa tapauksessa jack,queen,king tai ace
        """
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

    def filename(self):
        """Palauttaa kortin tiedostonimen

        Returns:
            Kortin tiedostonimi merkkijonona
        """
        return f"{self.alternative_rank()}_of_{self.suit.lower()}"

    def update(self):
        """Päivittää kortin kuvan jos se ei vastaa show-arvoa
        """
        if self.show != self.front_side_image:
            self.set_image()

    def __str__(self):
        """Muodostaa kortista merkkijonomuotoisen esityksen.

        Returns:
            Merkkijono, joka kertoo kortin arvon ja maan
        """
        return f"{self.rank} of {self.suit}"
