# Testausdokumentti

Ohjelmaa on testattu sekä automatisoiduin yksikkö- ja integraatiotestein unittestilla sekä manuaalisesti tapahtunein järjestelmätason testein.

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

Pelisilmukasta vastaavaa `GameLoop`-luokkaa testataan [TestGameLoop](https://github.com/pankalai/ot-harjoitustyo/blob/main/pasianssi-app/src/tests/services/game_loop_test.py)-testiluokalla. `GameLoop`-olio alustetaan niin, että sille injektoidaan riippuvuuksiksi game-, renderer-, eventqueue- ja clock-luokat. Tätä varten testissä on käytössä luokat `StubGame`, `StubRenderer`,`StubEventQueue` ja `StubClock`. Testeissä on käytetty hyväksi myös Mock-luokkaa varmistamaan, että oikeita metodeja kutsutaan oikeilla parametreilla. Mock-olio on toteutettu `StubGame`- ja `StubRenderer`-olioille.

Klondike-pelistä vastaavaa `Klondike`-luokkaa testataan [TestKlondike](https://github.com/pankalai/ot-harjoitustyo/blob/main/pasianssi-app/src/tests/services/klondike_test.py)-testiluokalla. 

Korttiryhmien hallinnasta vastaavaa `GroupHandler`-luokkaa testataan [TestGroupHandler](https://github.com/pankalai/ot-harjoitustyo/blob/main/pasianssi-app/src/tests/services/group_handler_test.py)-testiluokalla. Osittain sitä testataan myös `Klondike`-luokan testien yhteydessä. 

### Repositorio-luokka

Repositorio-luokkaa `GameRepository` testataan testeissä käytössäolevalla tietokannalla. Testitietokannan nimi on konfiguroitu _.env.test_-tiedostoon. `GameRepository`-luokkaa testataan [TestGameRepository](https://github.com/pankalai/ot-harjoitustyo/blob/main/pasianssi-app/src/tests/repositories/game_repository_test.py)-testiluokalla. Testeissä on käytössä `GameService`-luokan olio, joka alustetaan niin, että sille injektoidaan riippuvuuksiksi game- ja game loop -luokat. Tätä varten testissä on käytössä luokat `StubGame` ja `StubGameLoop`. 


### Testauskattavuus

Käyttöliittymäkerrosta lukuunottamatta sovelluksen testauksen haarautumakattavuus on 94%.

![](./kuvat/testikattavuus.png)

Testikattavuuden ulkopuolelle on jätetty paketin ui alla olevat tiedostot ja pelinäkymän piirtämisestä vastaava renderer-luokka. Myöskään _index.py_ ja _build.py_-tiedostoja ei ole testattu.

## Järjestelmätestaus

Sovelluksen järjestelmätestaus on suoritettu manuaalisesti.

### Asennus ja konfigurointi

Sovellus on haettu ja sitä on testattu [käyttöohjeen](./kayttoohje.md) kuvaamalla tavalla sekä Windows- että Linux-ympäristössä. 

### Toiminnallisuudet

Kaikki [määrittelydokumentin](./vaatimusmaarittely.md) ja käyttöohjeen listaamat toiminnallisuudet on käyty läpi ja todettu toimiviksi.


## Sovellukseen jääneet laatuongelmat

Sovellus ei anna tällä hetkellä järkeviä virheilmoituksia seuraavissa tilanteissa:

- Konfiguraation määrittelemään tiedostoon ei ole luku-/kirjoitusoikeutta
- SQLite tietokantaa ei ole alustettu, eli `python -m poetry run invoke build`-komentoa ei ole suoritettu
