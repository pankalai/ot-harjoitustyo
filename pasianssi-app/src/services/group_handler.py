from entities.card import Card


class GroupHandler:
    """Tietää missä ryhmässä kortti on 
    ja huolehtii korttien siirtämisestä ryhmästä toiseen 
    """

    def __init__(self):
        """Luokan konstruktori, joka luo uuden ryhmähallitsijan.
        """
        self.groups = {}

    def get_current_group(self, card: Card):
        """Palauttaa kortin nykyisen ryhmän

        Args:
            card (Card): Card-luokan olio

        Returns:
            Palauttaa ryhmän, jossa kortti on tai None, jos kortti ei ole missään ryhmässä
        """
        if card in self.groups:
            return self.groups[card]
        return None

    def remove_from_group(self, card: Card, group):
        """Poistaa kortin ryhmästä

        Args:
            card (Card): Poistettava kortti. Card-luokan olio.
            group (_type_): Korttiryhmä, josta poistetaan.
        """
        group.remove(card)

    def add_to_group(self, card: Card, group):
        """Lisää kortin ryhmään

        Args:
            card (Card): Lisättävä kortti. Card-luokan olio.
            group (_type_): Ryhmä, johon kortti lisätään
        """
        group.add(card)
        if card in self.groups:
            self.remove_from_group(card, self.groups[card])
        self.groups[card] = group

    def clear_groups(self):
        """Tyhjentää kaikki groups-objektista löytyvät ryhmät
        """
        group_set = set(values for values in self.groups.values())
        for group in group_set:
            group.clear()
