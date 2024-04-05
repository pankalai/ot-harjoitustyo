from entities.deck import Deck

class Klondike:
    """
    Klondike-pelin logiikasta vastaava luokka
    """
    def __init__(self, level = 3):
        self.deck = Deck()
        self.piles = [[] for _ in range(7)]
        self.foundations = [[] for _ in range(4)]
        self.stock = []
        self.waste = []

        if level == 1: 
            self.turning_cards = 1
        elif level == 3:
            self.turning_cards = 3
        
    def draw(self):
        self.deck.build()
        self.deck.shuffle()

        n = 1
        for i in range(len(self.piles)):
            self.piles[i] = self.deck.deal(n)
            n += 1

        self.stock = self.deck.cards.copy()
 
    def deal(self):
        if self.stock:
            for _ in range(min(self.turning_cards, len(self.stock))):
                self.waste.append(self.stock.pop())
        else:
            self.stock = self.waste.copy()
            self.waste.clear()

    def add_to_foundation(self, card, foundation_index):
        if self.card_valid_for_foundation(card, foundation_index):
            self.foundations[foundation_index].append(card)
            return True
        
        return False
            
    def add_to_pile(self, cards, pile_index):
        if self.card_valid_for_pile(cards[0], pile_index):
            for card in cards:
                self.piles[pile_index].append(card)
            return True
 
        return False
    
    def card_valid_for_foundation(self, card, foundation_index):
        if not self.foundations[foundation_index]:
            if card.value == 1:
                return True
        elif self.foundations[foundation_index][-1].suit == card.suit and self.foundations[foundation_index][-1].value == card.value-1:  
            return True
        
        return False

    def card_valid_for_pile(self, card, pile_index):
        if not self.piles[pile_index]:
            if card.value == 13: 
                return True  
        elif (self.piles[pile_index][-1].value == card.value+1 and  
            self.piles[pile_index][-1].color != card.color):
            return True
        
        return False
        

                    
                    


            

