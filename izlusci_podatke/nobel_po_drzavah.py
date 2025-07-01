import re
import csv
import requests
import os
from unidecode import unidecode

absolutna_pot = os.path.dirname(os.path.abspath(__file__))

# Nobelovi nagrajenci po državah

def podatki_o_drzavah1():
    # Preden se lotimo analize Nobelovih nagrajencev po državah, lahko izpostavimo število prebivalcev za vsako državo.
    url = "https://www.worldometers.info/world-population/population-by-country"
    r = requests.get(url)
    vsebina = r.text

    pot = os.path.join(absolutna_pot, "..", "podatki", "drzave_po_prebivalcih.html")
    with open(pot, "w", encoding="utf-8") as dat:
        dat.write(vsebina)

    vzorec = re.compile(
        r'>(?P<drzava>\D+?)</a> </td><td class="px-2 border-e border-zinc-200 ' 
        r'text-end py-1.5 border-b font-bold" data-order="(?P<stevilo>\d+)"'
                        )

    drzave_po_prebivalcih = {}
    for match in vzorec.finditer(vsebina):
        drzava = re.sub("&amp;", "and", match.group(1).strip())
        prebivalci = int(match.group(2))
        drzave_po_prebivalcih[drzava] = prebivalci

    pot = os.path.join(absolutna_pot, "..", "podatki", "drzave_po_prebivalcih.csv")
    with open(pot, "w", newline='', encoding="utf-8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["država", "število prebivalcev"])
        for drzava, prebivalci in drzave_po_prebivalcih.items():
            pisatelj.writerow([drzava, prebivalci])
    return drzave_po_prebivalcih

def podatki_o_drzavah2():
    # To je tretja spletna stran, s katere bomo shranjevali podatke in jih ustrezno analizirali.
    # Zaradi tega bomo ustvarili novo datoteko in kasneje podatke "normalizirali" z uporabo knjižnice pandas.
    # Od tod sprejmemo podatke o državah in nagrajencev.
    url = "https://www.britannica.com/topic/Nobel-Prize-Winners-by-Year-1856946"
    r = requests.get(url)
    vsebina = r.text

    pot = os.path.join(absolutna_pot, "..", "podatki", "nobel_po_drzavah.html")
    with open(pot, "w", encoding="utf-8") as dat:
        dat.write(vsebina)

    vzorec = re.compile(
        r'class="md-crosslink " data-show-preview="true">(?P<ime>.*?)</a>.*?</td><td>(?P<drzava>[^<]+)</td>'
                        )

    nobel_po_drzavah = {}

    # Ker je veliko nagrajencev, ki prihajajo iz držav, ki že ne obstajajo, bomo nekatere od teh držav ustrezno poimenovali.
    # In sicer, zaradi boljše analize in večjega števila podatkov, privzeli bomo da so vse nagrade za U.S.S.R. pravzaprav ruske.
    # Podobno lahko naredimo za Čehoslovaško.
    # Ker bomo tudi analizirali število prebivalcev z druge spletne strani, najbolj pomembne države bomo poimenovali kot so na tej strani.
    # Tudi za države kot so "Trinidad and Tobago" začetno "&amp;" ustrezno zamenjamo z "and".
    # Izognemo se tudi znakov kot so pika ali podpičje, pa še zahtevamo da, v primeru več držav za istega nagrajenca,
    # računalnik izbere prvo. Mislimo, da je tista najbolj pomembna. V tem primeru je med dvemi državami "-" ali "/".
    for match in vzorec.finditer(vsebina):
        ime = unidecode(match.group("ime").strip())
        drzava = re.sub(r'&amp;', 'and', match.group("drzava").strip())
        if "/" in drzava:
            drzava = drzava[:drzava.index("/")]
        if "-" in drzava:
            drzava = drzava[:drzava.index("-")]
        if drzava == "U.S.S.R.":
            drzava = "Russia"
        if drzava == "Phil.":
            drzava = "Phillipines"
        if drzava == "U.K.":
            drzava = "United Kingdom"
        if drzava == "U.S.":
            drzava = "United States"
        if drzava == "Neth.":
            drzava = "Netherlands"
        if drzava == "French":
            drzava = "France"
        if drzava == "Czechoslovakia":
            drzava = "Czech Republic (Czechia)"
        nobel_po_drzavah[ime] = drzava

    pot = os.path.join(absolutna_pot, "..", "podatki", "nobel_po_drzavah.csv")
    with open(pot, "w", newline='', encoding="utf-8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["nagrajenec", "država"])
        for ime in nobel_po_drzavah:
            pisatelj.writerow([ime, nobel_po_drzavah[ime]])
    return nobel_po_drzavah

def podatki_o_drzavah3():
    # Na podoben način shranimo vse podatke o državah v novi csv datoteki.
    # V njej bomo imeli skupno število nagrad za državo in še koliko tista država ima nagrad,
    # glede na 100 tisoč prebivalcev.
    # Opomnimo še, da niso vsi nagrajenci v novi datoteki, ampak jih je dovolj veliko,
    # da lahko rečemo, da gre za drobno analizo.
    drzave_po_nobelu = {}
    drzave_na_100 = {}
    nobel_po_drzavah = podatki_o_drzavah2()
    drzave_po_prebivalcih = podatki_o_drzavah1()
    
    for nagrajenec in nobel_po_drzavah:
    # Če je nagrajenec organizacija, potem ne piše država, ampak leto, v katerem je ustvarjena.
    # Zato se teh primerov izognimo in jih ne zapišemo v naši datoteki.
        if "founded" not in nobel_po_drzavah[nagrajenec] and nobel_po_drzavah[nagrajenec]:   
            drzave_po_nobelu[nobel_po_drzavah[nagrajenec]] = drzave_po_nobelu.get(nobel_po_drzavah[nagrajenec], 0) + 1

    # Če noben nagrajenec ne prihaja iz neke države, potem je število nagrajencev seveda 0.
    for drzava in drzave_po_prebivalcih:
        if drzava not in drzave_po_nobelu:
            drzave_po_nobelu[drzava] = 0

    # Ko računamo število nagrad na 100 tisoč prebivalcev, sprehajamo se po državah iz seznama s prebivalcima.
    # V nasprotnem primeru se lahko zgodi napaka, da recimo računalnik išče število prebivalcev Jugoslavije.
    for drzava in drzave_po_prebivalcih:
        nagrada_na_100 = (drzave_po_nobelu[drzava] / drzave_po_prebivalcih[drzava]) * (10 ** 5)
        drzave_na_100[drzava] = nagrada_na_100

    # Ustvarimo še zadnjo csv datoteko, kjer bomo shranili tiste podatke pomembne za analizu.
    pot = os.path.join(absolutna_pot, "..", "podatki", "podatki_o_drzavah.csv")
    with open(pot, "w", newline="", encoding="utf-8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["država", "skupno", "nagrade na prebivalce"])
        for drzava in drzave_po_prebivalcih:
            pisatelj.writerow([drzava, drzave_po_nobelu[drzava], drzave_na_100[drzava]])
    return drzave_po_nobelu, drzave_na_100