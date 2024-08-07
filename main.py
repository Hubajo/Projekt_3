"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Josef Hubáček
email: jos.hubacek@gmail.com
discord: jose9990552
"""

import sys
import requests
from bs4 import BeautifulSoup



def main(odkaz: str, nazev_souboru: str) -> None:
    # Hlavička souboru
    hlavicka = (
        "Číslo;Název;Voliči v seznamu;Vydané obálky;Volební účast v %;Odevzdané obálky;Platné hlasy; % platných hlasů;"
        "Občanská demokratická strana;Řád národa - Vlastenecká unie;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;"
        "Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;"
        "ROZUMNÍ-stop migraci,diktát.EU;Strana svobodných občanů;Blok proti islam.-Obran.domova;"
        "Občanská demokratická aliance;Česká pirátská strana;Referendum o Evropské unii;TOP 09;ANO 2011;"
        "Dobrá volba 2016;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;Česká strana národně sociální;"
        "REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů"
    )

    # Požadavek na daný web
    odpoved = requests.get(odkaz)
    print(f"Stahuji data z URL {odkaz}")
    print(f"Ukládám do souboru {nazev_souboru}")

    # Parsování stránek
    soup = BeautifulSoup(odpoved.text, "html.parser")

    # Vyhledání čísel a názvů obcí
    cislo_obce = soup.find_all("td", class_="cislo")
    nazev_obce = soup.find_all("td", class_="overflow_name")

    # Vytvoření zipu čísel a názvů obcí
    obce_zip = zip(cislo_obce, nazev_obce)

    # Otevření souboru a zapsání hlavičky
    with open(nazev_souboru, "w") as soubor:
        soubor.write(hlavicka + "\n")

        # Iterace přes zazipovaný seznam
        for cislo_obce, nazev_obce in obce_zip:
            # Vrací seznam dat získaných z URL, které jsou spojené s daným číslem obce
            tabulka_data = url_tag(cislo_obce)

            # Vytvoření řádku s daty obce
            radek = f"{cislo_obce.text};{nazev_obce.text};" + ";".join(tabulka_data) + "\n"
            
            # Zápis do souboru
            soubor.write(radek)

    print("Ukončuji Scraper")

# Funkce, která z tagu pro číslo obce vezme url
def url_tag(tag: BeautifulSoup) -> list:
    base_url = "https://volby.cz/pls/ps2017nss/"
    for url in tag('a', href=True):
        full_url = base_url + url.get('href')
        odpoved = requests.get(full_url)
        soup = BeautifulSoup(odpoved.text, "html.parser")
        return vysledky_hlasovani(soup)

# Funkce, která projde tabulky na URL daného okrsku, sebere data a přidá je do listu
def vysledky_hlasovani(soup: BeautifulSoup) -> list:
    data = []

    # Horní tabulka s voliči, hlasy a obálkami
    vysledky_horni = soup.find_all("td", class_="cislo")
    data.extend([atr.text for atr in vysledky_horni[3:9]])

    # Dolní tabulky s jednotlivými stranami a počty hlasů
    vysledky_dolni = soup.find_all("td", headers="t1sa2 t1sb3") + soup.find_all("td", headers="t2sa2 t2sb3")
    data.extend([atr.text for atr in vysledky_dolni[:-1]])

    return data

if __name__ == '__main__':
    try:
        url = str(sys.argv[1])
    except IndexError:
        print("Použili jste špatné URL.")
        quit()

    try:
        name = str(sys.argv[2])
    except IndexError:
        print("Chybný formát souboru.")
        quit()

    if not name.endswith(".csv"):
        print("Chybný formát souboru.")
        quit()

    if not url.startswith("https://volby.cz/pls/ps2017nss/"):
        print("Použili jste špatné URL")
        quit()

    main(url, name)