class GrabbedCards:
    def __init__(self):
        self.cards = []
        self.list_n = 0

    def key_object(self):
        return self.cards[0]

    def clear(self):
        self.cards.clear()

    def is_empty(self):
        return len(self.cards) == 0

    def add(self, card):
        self.cards.append(card)

    def move(self, rel):
        for card in self.cards:
            card.rect.move_ip(rel)

    def get_list(self):
        return self.cards

    def __iter__(self):
        self.list_n = 0
        return self

    def __next__(self):
        if self.list_n < len(self.cards):
            card = self.cards[self.list_n]
            self.list_n += 1
            return card
        raise StopIteration
