import os
import pygame

dirname = os.path.dirname(__file__)


class Card(pygame.sprite.Sprite):
    """Luokka, jonka avulla ylläpidetään tietoa yksittäisestä pelikortista.

    Args:
        Perii pygamen sprite-luokan.
    """

    def __init__(self, suit: str, rank: int, show: bool = False):
        """Luokan konstruktori, joka luo uuden pelikortin.

        Args:
            suit (str): Kortin maa.
            rank (int): Kortin arvo.
            show (bool, optional): Onko kortti näkyvissä eli kuvapuoli ylöspäin,
            oletusarvona kuvapuoli on alaspäin.
        """
        super().__init__()

        self.suit = suit
        self.rank = rank

        self.rect = None
        self.image = None

        self._show = show
        self._image_size = None
        self._front_side_image = None

    @property
    def color(self):
        """Palauttaa kortin värin.

        Returns:
            Tavanomaisen pakan tapauksessa punainen tai musta, muutoin None.
        """
        if self.suit in ("Diamonds", "Hearts"):
            return "red"
        if self.suit in ("Spades", "Clubs"):
            return "black"
        return None

    @property
    def is_visible(self):
        """Palauttaa tiedon onko kortti kuvapuoli ylöspäin vai alaspäin.

        Returns:
           True, jos ylöspäin, ja False, jos alaspäin. 
        """
        return self._show

    def flip(self):
        """Kääntää kortin ympäri.
        """
        self._show = not self._show

    def move(self, rel: tuple):
        """Siirtää korttia.

        Args:
            rel (tuple): Siirron suuruus x- ja y-koordinaatteina.
        """
        self.rect.move_ip(rel)

    def set_image_size(self, size: tuple):
        """Asettaa kortin kuvakoon.

        Args:
            size (tuple): Kortin koko tuplena (leveys, korkeus).
        """
        self._image_size = size
        self._set_image()

    def set_position(self, position: tuple):
        """Asettaa kortin sijainnin.

        Args:
            position (tuple): Kortin sijainti tuplena (vasen, ylä).
        """
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def get_position(self):
        """Palauttaa kortin sijainnin.

        Returns:
            Kortin vasemman yläkulman koordinaatit tuplena.
        """
        return self.rect.x, self.rect.y

    def _set_image(self):
        """Lataa kortin kuvan.
        """
        if self._show:
            image = pygame.image.load(
                os.path.join(dirname, "..", r"assets/cards",
                             self.filename() + ".png")
            )
            self._front_side_image = True
        else:
            image = pygame.image.load(
                os.path.join(dirname, "..", r"assets/cards", "back-side.png")
            )
            self._front_side_image = False

        self.image = pygame.transform.smoothscale(image, self._image_size)

    def update(self):
        """Päivittää kortin kuvan, jos se ei vastaa show-attribuutin arvoa.
        """
        if self._show != self._front_side_image:
            self._set_image()

    def _alternative_rank(self):
        """Palauttaa kuvakortin vaihtoehtoisen arvon. 
        Hyödynnetään kortin kuvan lataamisessa.

        Returns:
            Kortin arvo, jos kyseessä ei ole kuvakortti, muussa tapauksessa 
            jack, queen, king tai ace.
        """
        match self.rank:
            case 1:
                return "ace"
            case 11:
                return "jack"
            case 12:
                return "queen"
            case 13:
                return "king"
            case _:
                return self.rank

    def filename(self):
        """Palauttaa kortin tiedostonimen.

        Returns:
            Kortin tiedostonimi merkkijonona.
        """
        return f"{self._alternative_rank()}_of_{self.suit.lower()}"

    def __str__(self):
        """Muodostaa kortista merkkijonomuotoisen esityksen.

        Returns:
            Merkkijono, joka kertoo kortin arvon ja maan.
        """
        return f"{self.rank} of {self.suit}"
