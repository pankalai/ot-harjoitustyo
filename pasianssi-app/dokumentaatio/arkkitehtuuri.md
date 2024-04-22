## Sovelluslogiikka

```mermaid
 classDiagram
    Card "*" -- "1" Deck
    Klondike "1" -- "1" Deck
	Klondike "1" -- "1" GroupHandler
	Klondike "1" -- "6" CardGroup
    Klondike "1" -- "7" Pile
    CardGroup <|-- Pile
    GroupHandler ..|> Pile
    GroupHandler ..|> CardGroup
   class Card{
        rank
        suit
        color
        show
        size
        rect
        image
    }
    class Deck{
        cards
    }
    class Klondike{
        deck
        stack
        waste
        piles
        foundations
        turning_cards
    }
    class GroupHandler{
        groups
    }
    class CardGroup{
        cards
    }
```

## Toiminnallisuudet

### Kortin siirto peruspakkaan tuplaklikkaamalla

Kun käyttäjä tuplaklikkaa korttia, joka on kelvollinen siirrettäväksi johonkin neljästä peruspakasta, etenee sovelluksen kontrolli seuraavasti:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant Klondike
  participant GroupHandler
  User->>UI: double click card
  UI->>Klondike: add_to_foundation(card)
  loop foundations
        Klondike->>Klondike: valid_to_foundation(card,foundation)
    end
  Klondike->>GroupHandler: add_to_group(card,foundation)
  GroupHandler-->>Klondike: True
  Klondike-->>UI: True
  UI->>UI: update_waste()
  UI->>UI: update_piles()
  UI->>UI: update_foundations()

```