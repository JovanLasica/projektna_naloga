import re
import csv
import requests
import os
from unidecode import unidecode

absolutna_pot = os.path.dirname(os.path.abspath(__file__))

def zberi_osnovne_podatke():
    # Najprej si zapišimo url spletne strani, s katere bomo prenesli podatke in shranimo vsebino v zasebno datoteko.
    # Iz datoteke "nobelovi_nagrajenci.html" bomo prebrali podatke.
    url = "https://www.nobelprize.org/prizes/lists/all-nobel-prizes/all/"
    r = requests.get(url)
    vsebina = r.text

    with open("nobelovi_nagrajenci.html", "w", encoding="utf-8") as dat:
        dat.write(vsebina)

    # Z pomočjo analize vsebine smo ugotovili da je vzorec za vsakega nagrajenca izgleda kot spodaj.
    # Za lažje nadaljevanje vsako skupino podatkov ustrezno poimenujemo in označimo za kateri tip besedila gre (števila, črke, komplementi...).    
    vzorec = re.compile(
        r'href="https://www.nobelprize.org/prizes/(?P<podrocje>\D+)/(?P<leto>\d+)/(\D+)/facts/">\n(?P<oseba>\D+)</a>'
                        )

    nagrajenci = {}
    # Uporabimo unidecode, da se bodo imena na vsaki strani ujemala.
    # Na strani "nobelprize.org" so imena napisana v jeziku nagrajencev.
    # Seveda je v takih primerih boljše, da vse imamo v angleščini.
    for match in vzorec.finditer(vsebina):
        nagrajenec = unidecode(match.group("oseba").strip())
        podrocje = match.group("podrocje").strip()
        leto = int(match.group("leto").strip())
    # Tukaj se izognemo težav, v primeru da ena oseba ima več nagrad (kot recimo Marie Curie).
        if nagrajenec not in nagrajenci:   
            nagrajenci[nagrajenec] = [[podrocje, leto]]
        else:
            nagrajenci[nagrajenec].append([podrocje, leto])
        # Na koncu ustvarimo zasebno csv datoteko, oziroma tabelo, v kateri bodo shranjeni vsi nagrajenci po letu in področju.
        with open("nobelovi_nagrajenci.csv", "w", newline='', encoding="utf-8") as dat:
            pisatelj = csv.writer(dat)
            pisatelj.writerow(["nagrajenec", "področje", "leto"])
        # Sprehajamo se po vseh nagrad za fiksiranega nagrajenca.
        # Čeprav takih primerih ni veliko, ni problemov z efikasnostjo kode.
            for nagrajenec in nagrajenci:
                for i in range(len(nagrajenci[nagrajenec])):
                    pisatelj.writerow([nagrajenec, nagrajenci[nagrajenec][i][0], nagrajenci[nagrajenec][i][1]])
    return nagrajenci