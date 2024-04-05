class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
        if self.suit in ("Diamonds","Hearts"):
            self.color = "red"
        elif self.suit in ("Spades","Clubs"):
            self.color = "black"
        else:
            self.color = None

    def __str__(self):
        return f"{self.value} of {self.suit}"