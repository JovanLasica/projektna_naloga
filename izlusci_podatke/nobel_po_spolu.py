import csv
import os
import gender_guesser.detector as gender
detektor = gender.Detector()

absolutna_pot = os.path.dirname(os.path.abspath(__file__))

# Nobelovi nagrajenci po spolu

def podatki_o_spolu():
    # Ker ne obstaja spletna stran, na kateri je v razrepedelnici o nagrajencih stolpec "spol", prevzeli bomo
    # da so imena Nobelovih nagrajencev dovolj znana, da knjižnica gender_guesser ustrezno določi spol.
    # Če je spol "unknown", predpostavimo da tedaj gre za organizacijo (kot recimo "United Nations") in podobno.
    # V tem primeru, nagrajenca ne bomo shranili v datoteko. Zanimajo nas tisti, za katere poznamo spol.
    nobel_po_spolu = {}
    from .nobelovi_nagrajenci import zberi_osnovne_podatke
    nagrajenci = zberi_osnovne_podatke()

    for oseba in nagrajenci:
    # Vse besede v imenu osebe ločimo v seznam.
            sez = oseba.split()
            if sez[0].lower() != "sir":
                spol = detektor.get_gender(sez[0])
            else:
                spol = detektor.get_gender(sez[1])
    # Tudi se lahko zgodi da spol označi z "mostly-(fe)male", kar nočemo, zato naj rečemo da,
    # če je "female" znotraj spola, potem je to "female", sicer je "male".
            if spol != "unknown":
                if "female" in spol:
                    nobel_po_spolu[oseba] = "female"
                else:
                    nobel_po_spolu[oseba] = "male"

    # Ustvarjimo csv razpredelnico z dva stolpca, ki jo bomo kasneje uporabili.
    pot = os.path.join(absolutna_pot, "..", "podatki", "nobel_po_spolu.csv")
    with open(pot, "w", newline='', encoding="utf-8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["nagrajenec", "spol"])
        for oseba in nobel_po_spolu:
            pisatelj.writerow([oseba, nobel_po_spolu[oseba]])
    return nobel_po_spolu