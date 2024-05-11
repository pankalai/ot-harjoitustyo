from entities.card import Card


class GroupHandler:
    """Tietää missä ryhmässä kortti on ja huolehtii korttien 
    siirtämisestä ryhmästä toiseen.
    """

    def __init__(self):
        """Luokan konstruktori, joka luo uuden ryhmähallitsijan.
        """
        self._groups = {}

    def get_current_group(self, card: Card):
        """Palauttaa kortin nykyisen ryhmän.

        Args:
            card (Card): Kortti, jonka ryhmä haetaan.

        Returns:
            Palauttaa ryhmän, jossa kortti on tai None, jos kortti ei ole missään ryhmässä.
        """
        if card in self._groups:
            return self._groups[card]
        return None

    def add_to_group(self, card: Card, group):
        """Lisää kortin ryhmään.

        Args:
            card (Card): Lisättävä kortti.
            group: Ryhmä, johon kortti lisätään.
        """
        group.add(card)
        if card in self._groups:
            remove_from_group(card, self._groups[card])
        self._groups[card] = group

    def clear_card_groups(self):
        """Tyhjentää kaikki groups-objektista löytyvät ryhmät.
        """
        group_set = set(values for values in self._groups.values())
        for group in group_set:
            group.clear()

    def clear_groups(self):
        """Tyhjentää ylläpitämänsä sanakirjan.
        """
        self._groups.clear()


def remove_from_group(card: Card, group):
    """Poistaa kortin ryhmästä.

    Args:
        card (Card): Poistettava kortti.
        group: Korttiryhmä, josta poistetaan.
    """
    group.remove(card)
