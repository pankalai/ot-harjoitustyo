# Ohjelmistotekniikka, harjoitustyö

## Pasianssi

- [Vaatimusmäärittely](./pasianssi-app/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](./pasianssi-app/dokumentaatio/arkkitehtuuri.md)
- [Työaikakirjanpito](./pasianssi-app/dokumentaatio/tuntikirjanpito.md)
- [Muutosloki](./pasianssi-app/dokumentaatio/changelog.md)


# Asennus

1. Asenna riippuvuudet komennolla:
```
poetry install
```

2. Käynnistä sovellus komennolla:
```
poetry run invoke start
```


# Komentorivitoiminnot

## Ohjelman suorittaminen

Ohjelman pystyy suorittamaan komennolla:

```
poetry run invoke start
```

## Testaus

Testit suoritetaan komennolla:
```
poetry run invoke test
```

## Testikattavuus

Testikattavuusraportin voi generoida komennolla:
```
poetry run invoke coverage-report
```
Raportti generoituu htmlcov-hakemistoon.

## Pylint

Tiedoston .pylintrc määrittelemät tarkistukset voi suorittaa komennolla:
```
poetry run invoke lint
```
