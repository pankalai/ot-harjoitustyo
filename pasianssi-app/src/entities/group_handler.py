class GroupHandler:
    """
    Tietää missä ryhmässä kortti sijaitsee.
    Siirrettäessä uuteen ryhmään kortti poistuu vanhasta ryhmästä.
    """

    def __init__(self):
        self.group = {}

    def get_current_group(self, card):
        if card in self.group:
            return self.group[card]
        return None

    def add_to_group(self, card, group):
        if group.add(card):
            if card in self.group:
                old_group = self.group[card]
                old_group.remove(card)
            self.group[card] = group
            return True
        return False
