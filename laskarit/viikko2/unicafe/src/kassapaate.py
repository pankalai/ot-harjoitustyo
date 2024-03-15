class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0
        self.hinnat = {"edullinen":240, "maukas":400}

    def syo_edullisesti_kateisella(self, maksu):
        return self.maksa_kateisella(maksu,"edullinen")

    def syo_maukkaasti_kateisella(self, maksu):
        return self.maksa_kateisella(maksu,"maukas")

    def syo_edullisesti_kortilla(self, kortti):
        return self.maksa_kortilla(kortti,"edullinen")

    def syo_maukkaasti_kortilla(self, kortti):
        return self.maksa_kortilla(kortti,"maukas")

    def maksa_kateisella(self,maksu,tyyppi):
        if maksu >= self.hinnat[tyyppi]:
            self.kassassa_rahaa = self.kassassa_rahaa + self.hinnat[tyyppi]
            self.kasvata_myytyja_lounaita(tyyppi)
            return maksu - self.hinnat[tyyppi]
        else:
            return maksu
        
    def maksa_kortilla(self, kortti, tyyppi):
        if kortti.saldo >= self.hinnat[tyyppi]:
            kortti.ota_rahaa(self.hinnat[tyyppi])
            self.kasvata_myytyja_lounaita(tyyppi)
            return True
        else:
            return False
        
    def kasvata_myytyja_lounaita(self,tyyppi):
        if tyyppi == "maukas":
            self.maukkaat += 1
        else:
            self.edulliset += 1   
        
    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.kassassa_rahaa += summa
        else:
            return

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100
