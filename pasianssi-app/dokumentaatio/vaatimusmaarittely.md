# Vaatimusmäärittely

## Sovelluksen tarkoitus

Pasianssin (Klondike) pelaaminen. Eri vaikeustasoja. Sovellus tallettaa tietoa pelatuista peleistä, mikä mahdollistaa omien pelitulosten parantamisen ja vertailun muiden tuloksiin.

## Käyttäjät

Yksi käyttäjärooli eli pelaaja. Pelaaja voi antaa nimimerkin, jolla pelatun pelin tiedot tallentuvat tietokantaan. Jos pelaaja ei anna nimimerkkiä tietokannassa ja tilastoissa nimenä näkyy "anonyymi".

## Käyttöliittymäluonnos

Aloitusnäkymä. Luonnoksesta poiketen nimimerkki kirjoitetaan suoraan aloitusnäkymän nimimerkki-kenttään eikä aiemmin käytettyjä nimimerkkejä pääse katsomaan.

![](./kuvat/kayttoliittyma_hahmotelma1.png)

Pelinäkymä

![](./kuvat/kayttoliittyma_hahmotelma2.png)

## Toiminnallisuus

Käyttäjä voi valita helpon tai vaikean pelin. Helpossa kortteja käännetään yksi kerrallaan, vaikeassa kolme kerrallaan. Pelaaja siirtää kortteja pakasta toiseen raahaamalla. Kortti on mahdollista siirtää ns. peruspakkaan myös tuplaklikkaamalla. Pelin aikana näytöllä näkyy tehtyjen siirtojen määrä ja kulunut aika. Kyseiset tiedot tallentuvat kun peli menee läpi tai kun pelaaja lopettaa pelin (sulkemalla pelinäkymän).

Tarkempi kuvaus pelin toiminnallisuuksista:
- Pelaaja voi antaa nimimerkin [TEHTY]
- Pelaaja voi valita helpon tai vaikean pelin [TEHTY]
- Käsipakasta voi kääntää kortteja niin että maksimissaan kolme korttia kerrallaan on näkyvissä [TEHTY]
- Tuplaklikkaamalla korttia sen voi siirtää käsipakasta tai pinosta peruspakkaan [TEHTY]
- Kun kortti/kortteja on siirretty pois pinosta, päällimmäinen kortti kääntyy automaattisesti [TEHTY]
- Kortin voi siirtää raahaamalla pinosta peruspakkaan tai peruspakasta pinoon [TEHTY]
- Raahaamalla voi siirtää yhden tai usemman kortin pinosta toiseen [TEHTY]
- Tyhjään pinoon voi siirtää kuninkaan [TEHTY]
- Kulunut aika näkyy pelin aikana [TEHTY]
- Siirron jälkeen siirtojen määrä päivittyy näytölle [TEHTY]


## Jatkokehitysideoita

Mahdollisuus pelata muitakin pasiansseja, esim. Spider. Pelin valinta tehdään aloitusnäkymässä. Pelistä riippumatta vaihtoehtoina on helppo ja vaikea peli.
