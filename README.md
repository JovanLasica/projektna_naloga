# Analiza podatkov o Nobelovih nagrajencih

Ta projekt izvaja zajem in obdelavo podatkov o Nobelovih nagrajencih s pomočjo spletnega zajemanja.
Cilj je analizirati nagrajence po področjih, državah, univerzah, letu, itn.
Tudi bomo analizirali države, glede na število prebivalcev in Nobelovih nagrajencev.

## Zajem podatkov

Projekt uporablja podatke iz javno dostopnih spletnih strani: nobelprize.org, Wikipedia, Britannica, Worldometers.

## Struktura projekta

Projektna naloga/  
├── izlusci_podatke/  
│ ├── init.py  
│ ├── .gitignore.py  
│ ├── nobelovi_nagrajenci.py  
│ ├── nobelo_po_drzavah.py  
│ ├── nobelo_po_spolu.py  
│ └── nobelo_po_univerzah.py  
├── podatki/  
| ├── drzave_po_prebivalcih.html  
| ├── drzave_po_prebivalcih.csv  
| ├── nobel_po_drzavah.csv  
| ├── nobel_po_drzavah.html  
| ├── nobel_po_spolu.csv  
| ├── nobel_po_univerzah.csv  
| ├── nobel_po_univerzah.html  
| ├── nobelovi_nagrajenci.csv  
| ├── nobelovi_nagrajenci.html  
| ├── podatki_o_drzavah.csv
| └── skupna_tabela.csv  
├── analiza_podatkov.ipynb
├── main.py  
└── README.md

V glavni mapi Projektna naloga so mapi izlusci_podatke in podatki.
V mapi izlusci_podatke se nahajajo .py datoteke. V teh datotekah smo zajeli podatke sa spleta.
Tudi smo na ta način ostvarili nove .csv in .html datoteke, ki so v mapi podatki. Z uporabo teh, podatke bomo analizirali.
V glavni mapi imamo še tri datoteke. Ena izmed njih je README.md in v njej so navodila za zagon programa.
Druga je analiza_podatkov.ipynb, kjer smo z pomočjo Jupyter Notebooka analizirali podatke.
Tretja je main.py, z pomočjo nje poženemo program.  

### Opomba

Datoteko skupna_tabela.csv smo prenesli z interneta kot že pripravljeno, da bi shranili podatke o letih rojstva in smrti nagrajencev. Obstajali so tudi drugi načini, vendar niso bili zanesljivi za zbiranje dovolj velike količine podatkov za dobro analizo.

## Uporabljene knjižnice

Uporabnik za zagon programa mora imeti nameščene knjižnice:  

- requests (za zajem podatkov);  
- os (za pot do datotek);  
- re (za iskanje z pomočjo regularnih izrazov);  
- csv (za ustvarjanje csv datotek);  
- unidecode (za enolično in konsistentno pisanje imen);  
- gender_guesser (za analizo spola);  
- pandas (v Jupyter Notebooku).

## Zagon projekta

Uporabnik naj požene main.py, ki bo ustvaril vse potrebne datoteke.
Tiste bodo shranjene v mapi /podatki.
Na koncu odpremo analiza_podatkov.ipynb in izvedemo analizo.
