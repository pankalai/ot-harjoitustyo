# Vaatimusmäärittely

## Sovelluksen tarkoitus

Pasianssin (Klondike) pelaaminen. Eri vaikeustasoja. Sovellus tallettaa tietoa pelatuista peleistä, mikä mahdollistaa omien pelitulosten parantamisen ja vertailun muiden tuloksiin.

## Käyttäjät

Yksi käyttäjärooli eli pelaaja. Pelaaja voi käyttää aiemmin luotua nimimerkkiä tai luoda uuden. Tiedot peleistä tallentuvat nimimerkin mukaan.

## Käyttöliittymäluonnos

Aloitusnäkymä

![](./kuvat/kayttoliittyma_hahmotelma1.png)

Pelinäkymä

![](./kuvat/kayttoliittyma_hahmotelma2.png)

## Toiminnallisuus

Käyttäjä voi valita helpon tai vaikean pelin. Helpossa kortteja käännetään yksi kerrallaan, vaikeassa kolme kerrallaan. Pelaaja siirtää kortteja pakasta toiseen raahaamalla. Kortti on mahdollista siirtää ns. peruspakkaan myös tuplaklikkaamalla. Pelin aikana näytöllä näkyy tehtyjen siirtojen määrä ja kulunut aika. Nämä tiedot tallentuvat kun peli menee läpi tai kun pelaaja lopettaa pelin (sulkemalla sovelluksen tai aloittamalla uuden pelin).

Tarkempi kuvaus pelin toiminnallisuuksista:
- Käsipakasta voi kääntää kortteja niin että kolme korttia kerrallaan on näkyvissä [TEHTY]
- Tuplaklikkaamalla korttia sen voi siirtää käsipakasta tai pinosta peruspakkaan [TEHTY]
- Kun kortti/kortteja on siirretty pois pinosta, päällimmäinen kortti kääntyy [TEHTY]
- Kortin voi siirtää raahaamalla pinosta peruspakkaan tai peruspakasta pinoon
- Raahaamalla voi siirtää yhden tai usemman kortin pinosta toiseen 
- Siirron jälkeen siirtojen määrä päivittyy näytölle


## Jatkokehitysideoita

Mahdollisuus pelata muitakin pasiansseja, esim. Spider.
