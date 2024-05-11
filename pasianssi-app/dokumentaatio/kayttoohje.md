# Käyttöohje

Lataa projektin viimeisimmän [releasen](https://github.com/pankalai/ot-harjoitustyo/releases/) lähdekoodi valitsemalla _Assets_-osion alta _Source code_.


## Ohjelman käynnistäminen

Ennen ohjelman käynnistämistä asenna riippuvuudet komennolla

```bash
poetry install
```

Sen jälkeen suorita alustustoimenpiteet komennolla
```bash
poetry run invoke build
```

Näiden jälkeen ohjelman voi käynnistää komennolla

```
poetry run invoke start
```

## Nimimerkin antaminen ja vaikeustason valinta

Sovellus avautuu näkymään, jossa voi antaa nimimerkin ja valita joko helpon tai vaikean tason. Tilastoja parhaiten pelatuista peleistä voi katsoa klikkaamalla "Katso tilastoja".

![](./kuvat/aloitusnakyma.png)


## Pelaaminen

Pelin  tarkoituksena on järjestää kortit maittain suuruusjärjestykseen neljään peruspakkaan, jotka ovat pelin alussa tyhjiä. Pelin tavoitteen saavuttamiseksi käytössä ovat seuraavat toiminnot:
- Vasemman reunan käsipakasta voi kääntää kortteja klikkaamalla pakan kuvaa. Kääntyvien korttien määrä riippuu pelin vaikeustasosta. 
- Käännetyistä korteista ainoastaan päällimmäisen kortin voi siirtää joko johonkin pinoon tai suoraan peruspakkaan.
- Pinoon asetettavan kortin tulee olla vastakkaista väriä ja arvoltaan yhden pienempi kuin pinon päällimmäinen kortti. 
- Kortteja voi siirtää myös pinosta toiseen tai peruspakasta takaisin pinoon. 
- Tyhjään pinoon alimmaksi kortiksi tulee asettaa kuningas. 
- Kortin siirto peruspakkaan onnistuu myös tuplaklikkaamalla.

![](./kuvat/pelinakyma.png)

## Pelin lopettaminen

Pelin voi lopettaa painamalla oikean yläkulman ruksia ja valitsemalla "Palaa alkuun". 

![](./kuvat/viestinakyma.png)

## Ohjelman sulkeminen

Ohjelmasta poistutaan painamalla aloitusnäkymässä oikean yläkulman ruksia.