## Viikko 3

- Lisätty Card-luokka, joka vastaa korteista
- Lisätty Deck-luokka, joka vastaa korttipakasta
- Testattu, että korttipakkaa voi sekoittaa ja että siitä voi jakaa kortteja


## Viikko 4

- Laajennettu Card-luokkaa siten, että se perii Sprite-luokan
- Laajennettu pelin logiikasta vastaavaa Klondike-luokkaa ja tehty testejä
- Lisätty KlondikeView-luokka, joka vastaa pelin käyttöliittymästä
- Lisätty käyttöliittymään korttien kuvakkeet
- Lisätty StartView-luokka, joka tarjoaa mahdollisuuden valita helppo tai vaikea peli
- Pelaaja voi kääntää kortteja pakasta
- Pelaaja voi tuplaklikkaamalla siirtää kortteja peruspakkaan

## Viikko 5
- Lisätty CardGroup-luokka, joka vastaa yksittäisestä pinosta
- Lisätty GroupHandler-luokka, joka vastaa korttien siirtämisestä pinosta toiseen
- Lisätty GrabbedCards-luokka, joka vastaa käyttöliittymässä korttien siirtämisestä
- Lisätty Button-luokka, joka vastaa käyttöliittymän painikkeista
- Pelaaja voi siirtää kortteja raahaamalla pinosta toiseen ja peruspakkaan tai peruspakasta takaisin pinoon

## Viikko 6
- Lisätty Element-luokka, joka toimii yliluokkana käyttöliittymän objekteille, esimerkiksi painikkeille ja tekstikentälle
- Pelaaja voi antaa nimimerkin
- Pelaaja näkee tehtyjen siirtojen määrän ja pelikellon

## Viikkot 7
- Lisätty GameService-luokka, joka huolehtii pelisilmukan käynnistämisestä ja tietojen tallentamisesta tietokantaan.
- Lisätty GameLoop-luokka pelisilmukalle.
- Lisätty Eventqueue-luokka pygamen tapahtumajonon palauttamiseen.
- Lisätty Clock-luokka, joka vastaa aikaan liittyvistä toiminnoista.
- Lisätty Renderer-luokka, joka piirtää pelin näkymän.
- Pelaaja näkee kaikkien pelaajien parhaat tulokset.