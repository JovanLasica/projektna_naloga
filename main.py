from izlusci_podatke.nobelovi_nagrajenci import zberi_osnovne_podatke
from izlusci_podatke.nobel_po_drzavah import podatki_o_drzavah1, podatki_o_drzavah2, podatki_o_drzavah3
from izlusci_podatke.nobel_po_univerzah import podatki_o_univerzah
from izlusci_podatke.nobel_po_spolu import podatki_o_spolu

# V tej datoteki poženemo program in shranimo vse funkcije.
def main():
    osnovni_podatki = zberi_osnovne_podatke()
    drzave_po_prebivalcih = podatki_o_drzavah1()
    nobel_po_drzavah = podatki_o_drzavah2()
    drzave_nobel = podatki_o_drzavah3()
    univerze = podatki_o_univerzah()
    spol = podatki_o_spolu()
    

if __name__ == "__main__":
    main()