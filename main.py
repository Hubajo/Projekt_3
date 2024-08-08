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
    """Hlavní funkce pro stahování a zpracování dat."""
    hlavička = vytvor_hlavicku()
    print(f"Stahuji data z URL {odkaz}")
    print(f"Ukládám do souboru {nazev_souboru}")

    soup = stahni_a_parsuj(odkaz)
    obce_data = ziskej_data_obci(soup)

    uloz_do_souboru(nazev_souboru, hlavička, obce_data)
    print("Ukončuji Scraper")


def vytvor_hlavicku() -> str:
    """Vytvoří hlavičku pro CSV soubor."""
    return (
        "Číslo;Název;Voliči v seznamu;Vydané obálky;Volební účast v %;"
        "Odevzdané obálky;Platné hlasy; % platných hlasů;"
        "Občanská demokratická strana;Řád národa - Vlastenecká unie;"
        "CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;"
        "Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;"
        "Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;"
        "Strana svobodných občanů;Blok proti islam.-Obran.domova;"
        "Občanská demokratická aliance;Česká pirátská strana;"
        "Referendum o Evropské unii;TOP 09;ANO 2011;Dobrá volba 2016;"
        "SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;"
        "Česká strana národně sociální;REALISTÉ;SPORTOVCI;"
        "Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);"
        "Strana Práv Občanů"
    )


def stahni_a_parsuj(odkaz: str) -> BeautifulSoup:
    """Stáhne HTML stránku a vrátí její parsovanou podobu."""
    odpoved = requests.get(odkaz)
    return BeautifulSoup(odpoved.text, "html.parser")


def ziskej_data_obci(soup: BeautifulSoup) -> list:
    """Získá čísla a názvy obcí."""
    cislo_obce = soup.find_all("td", class_="cislo")
    nazev_obce = soup.find_all("td", class_="overflow_name")
    return list(zip(cislo_obce, nazev_obce))


def uloz_do_souboru(nazev_souboru: str, hlavička: str, obce_data: list) -> None:
    """Uloží data do souboru."""
    with open(nazev_souboru, "w") as soubor:
        soubor.write(hlavička + "\n")
        for cislo_obce, nazev_obce in obce_data:
            tabulka_data = url_tag(cislo_obce)
            radek = f"{cislo_obce.text};{nazev_obce.text};" + ";".join(tabulka_data) + "\n"
            soubor.write(radek)


def url_tag(tag: BeautifulSoup) -> list:
    """Vrátí URL a získá výsledky hlasování pro danou obec."""
    base_url = "https://volby.cz/pls/ps2017nss/"
    for url in tag('a', href=True):
        full_url = base_url + url.get('href')
        soup = stahni_a_parsuj(full_url)
        return vysledky_hlasovani(soup)


def vysledky_hlasovani(soup: BeautifulSoup) -> list:
    """Získá výsledky hlasování z dané stránky."""
    data = []
    vysledky_horni = soup.find_all("td", class_="cislo")
    data.extend([atr.text for atr in vysledky_horni[3:9]])
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