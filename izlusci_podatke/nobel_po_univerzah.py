import re
import csv
import requests
import os
from unidecode import unidecode

absolutna_pot = os.path.dirname(os.path.abspath(__file__))

# Nobelovi nagrajenci po univerzah

def podatki_o_univerzah():
    # Podobno kot prej shranimo podatke o nagrajencih in ustvarimo novo csv datoteko.
    # Pišemo novo datoteko, da se izognemo težav za tiste, ki mogoče niso naredili fakultete, ali za organizacije, ki so dobile nagrado.
    # Tudi ne vemo, ali za vse nagrajence sploh obstajajo podatki na tej strani.
    # Pomembno je, da to ni ista stran z katere smo prebrali osnovne podatke. Zato se mogoče podaci razlikujejo.
    url = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_university_affiliation"
    r = requests.get(url)
    vsebina = r.text

    pot = os.path.join(absolutna_pot, "..", "podatki", "nobel_po_univerzah.html")
    with open(pot, "w", encoding="utf-8") as dat:
        dat.write(vsebina)

    vzorec = re.compile(
        r'<span class="fn"><a href="/wiki/.+" title=".+">(?P<ime>\D+)</a></span></span></span>'
        r'\n</td>\n<td>.*\n</td>\n<td>\d+\n</td>\n.*title=".*">(?P<univerza>.+)</a>'
        )

    univerze = {}

    for match in vzorec.finditer(vsebina):
        ime = unidecode(match.group("ime").strip())
        univerza = match.group("univerza").strip()
        univerze[ime] = univerza

    pot = os.path.join(absolutna_pot, "..", "podatki", "nobel_po_univerzah.csv")
    with open(pot, "w", newline='', encoding="utf-8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["nagrajenec", "univerza"])
        for ime in univerze:
            pisatelj.writerow([ime, univerze[ime]])
    return univerze