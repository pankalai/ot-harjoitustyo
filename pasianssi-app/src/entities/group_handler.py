class GroupHandler:
    """
    Tietää missä ryhmässä kortti sijaitsee.
    Siirrettäessä uuteen ryhmään kortti poistuu vanhasta ryhmästä.
    """

    def __init__(self):
        self.groups = {}

    def get_current_group(self, card):
        if card in self.groups:
            return self.groups[card]
        return None

    def add_to_group(self, card, group):
        if group.add(card):
            if card in self.groups:
                old_group = self.groups[card]
                old_group.remove(card)
            self.groups[card] = group
            return True
        return False
