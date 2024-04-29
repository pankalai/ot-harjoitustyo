# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne noudattaa kolmitasoista kerrosarkkitehtuuria, ja koodin rakenne on seuraava:


Pakkaus ui sisältää käyttöliittymästä, services sovelluslogiikasta ja repositories tietojen pysyväistallennuksesta vastaavan koodin. Pakkaus entities sisältää luokkia, jotka kuvastavat sovelluksen käyttämiä tietokohteita.

## Käyttöliittymä

Käyttöliittymä sisältää kolme erilaista näkymää:

    Aloitusnäkymä
    Pelinäkymä
	Viestinäkymä
	
Näkymien näyttämisestä vastaa UI-luokka siten että yksi näytöistä on kerrallaan näkyvissä. Näkymät on toteutettu omina luokkinaan. Aloitusnäkymässä voi antaa nimimerkin ja valita pelin vaikeustason. Pelinäkymässä pelataan itse peliä. Viestinäkymä tulee näkyviin, kun peli menee läpi tai kun pelaaja haluaa lopettaa pelin. Tällöin pelaaja voi valita, haluaako palata aloitusnäkymään vai jatkaa pelaamista.


## Sovelluslogiikka

Sovelluksen loogisen tietomallin muodostavat luokat:

-Klondike: Pelin logiikasta vastaava luokka.

-GroupHandler: Luokka, joka vastaa korttien siirrosta ryhmästä toiseen.

-CardGroup: Korttiryhmästä vastaava luokka.

-Pile: Pinosta vastaava luokka. Perii luokan CardGroup. 

-Deck: Korttipakasta vastaava luokka. 

-Card: Yksittäisesta kortista vastaava luokka.

```mermaid
 classDiagram
    Card "*" -- "1" Deck
    Klondike "1" -- "1" Deck
	Klondike "1" -- "1" GroupHandler
	Klondike "1" -- "6" CardGroup
    Klondike "1" -- "7" Pile
    CardGroup <|-- Pile
    GroupHandler .. CardGroup
    CardGroup .. Card
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

Hakemistorakennetta kuvaava pakkauskaavio

```mermaid
 classDiagram
   ui ..|> services
   services ..|> repositories
   services ..|> entities

    class ui{
        StartView
        KlondikeView
        MessageView
    }
    class services{
        Klondike
       GroupHandler
    }
    class repositories{
        GameRepository
    }
    class entities{
        Deck
        CardGroup
        Pile
        Card
    }
```


## Tietojen pysyväistallennus

Pakkauksen repositories-luokka GameRepository huolehtii tietojen tallettamisesta SQLite-tietokantaan.


## Päätoiminnallisuudet

### Kortin/korttien kääntö käsipakasta
Kun käyttäjä klikkaa käsipakkaa, jossa on kortteja jäljellä, etenee sovelluksen kontrolli seuraavasti:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant Klondike
  participant GroupHandler
  User->>UI: click stack_area
  UI->>Klondike: deal()
  Klondike->>CardGroup: is_empty()
  CardGroup-->>Klondike: False
  Klondike->>CardGroup: get_top_cards(1)
  CardGroup-->>Klondike: card
  Klondike->>GroupHandler: add_to_group(card, waste)
  GroupHandler->>CardGroup: add(card)
  GroupHandler->>CardGroup: remove_from_group(card, stack)
  Klondike->>Card: flip(card)
 

  
```

### Kortin/korttien siirto pinosta toiseen
Kun käyttäjä siirtää yhden tai useamman kortin pinosta toiseen, etenee sovelluksen kontrolli seuraavasti:
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant Klondike
  participant GroupHandler
  User->>UI: click card
  UI->>UI: card=clicked_sprite(position)
  
  UI->>UI: create_grabbed_object(card)
  UI->>Klondike: get_sub_cards(card)
  Klondike->>GroupHandler: get_current_group(card)
  GroupHandler-->>Klondike: group
  Klondike->>CardGroup: get_sub_cards(card)
  CardGroup-->>Klondike: cards
  Klondike-->>UI: cards
  UI->>GrabbedCards: add(card)
  UI->>GrabbedCards: bottom_card()
  GrabbedCards-->>UI: card
  UI->>UI: check_collision(card)
  UI->>Klondike: add_to_pile(cards,pile)
  Klondike->>Klondike: valid_to_pile(cards[0],pile)
  Klondike->>GroupHandler: add_to_group (card,pile)
  GroupHandler->>CardGroup: add(card)
  GroupHandler->>CardGroup: remove_from_group(card, group)
```

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