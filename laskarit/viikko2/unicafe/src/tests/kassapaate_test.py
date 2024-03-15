import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti1 = Maksukortti(1000)
        self.maksukortti2 = Maksukortti(100)

    def test_rahamaara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000)
    
    def test_myytyjen_lounaiden_maara_on_oikea(self):
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.edulliset,0)

    def test_kateinen_kassa_kasvaa_lounaan_hinnalla(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1002.4)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1006.4)

    def test_kateinen_vaihtorahan_suuruus_oikea(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500),260)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500),100)

    def test_kateinen_myytyjen_lounaiden_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset,1)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.maukkaat,1)

    def test_kateinen_kassa_ei_kasva_jos_maksu_ei_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.maukkaat,0)

    def test_kateinen_kaikki_rahat_palautetaan_jos_maksu_ei_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100),100)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(100),100)

    def test_kateinen_myytyjen_lounaiden_maara_ei_muutu_jos_maksu_ei_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.maukkaat,0)

    def test_maksukortti_summa_veloitetaan_kortilta(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti1)
        self.assertEqual(self.maksukortti1.saldo_euroina(),7.6)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti1)
        self.assertEqual(self.maksukortti1.saldo_euroina(),3.6)

    def test_maksukortti_myytyjen_lounaiden_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti1)
        self.assertEqual(self.kassapaate.edulliset,1)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti1)
        self.assertEqual(self.kassapaate.maukkaat,1)

    def test_maksukortti_ei_tarpeeksi_rahaa_kortin_rahamaara_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti2)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti2)
        self.assertEqual(self.maksukortti2.saldo_euroina(),1.0)

    def test_maksukortti_ei_tarpeeksi_rahaa_lounaiden_maara_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti2)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti2)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.maukkaat,0)

    def test_maksukortti_kassan_rahamaara_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti1)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)

    def test_maksukortti_lataus_kortin_rahamaara_kasvaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti2,500)
        self.assertEqual(self.maksukortti2.saldo_euroina(),6.0)

    def test_maksukortti_lataus_kassa_kasvaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti2,500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1005.0)

    def test_maksukortti_lataus_kassa_ei_kasva_jos_negatiivinen_arvo(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti2,-500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)