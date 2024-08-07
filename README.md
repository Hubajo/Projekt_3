
Třetí projekt na Python Akademii od Engeta

POPIS PROJEKTU
Projekt umožňuje stáhnout a extrahovat výsledky z parlamentních voleb v roce 2017, z odkazu https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ kde si vybereme konkrétní okresek a následně obec, např. Olomoucký kraj a Olomouc


INSTALACE KNIHOVEN
Knihovny, které jsou použity, jsou uložené v souboru requirements.txt. V tomto projektu byly konkrétně využity knihovny requests a BeatifulSoup. Pro instalaci je vhodné vytvořit nové virtuální prostředí a následně instalovat každou zvlášť pomocí pip install název_knihovny nebo všechny pomocí pip install -r requirements.txt 

SPUŠTĚNÍ PROJEKTU
Spuštění souboru main.py např. ve Windows PowerShell vyžaduje dva povinné argumenty - odkaz a název souboru.
Postup v PowerShellu začíná příkazem: cd cesta_k_souboru např. cd C:\Users\PC\Desktop\projekt_engeto a následně spuštěním projektu: python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102" vysledky.csv

PRŮBĚH STAHOVÁNÍ
Stahuji data z url https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102
Ukládám do souboru vysledky.csv
Ukončuji Scraper

UKÁZKA
Číslo	Název	Voliči v seznamu	Vydané obálky	Volební účast v %	Odevzdané obálky
552356	Babice	    370	            256	                69,19	            256
500526	Bělkovice-Lašťany	1 801	1 079	            59,91	            1 078
500623	Bílá Lhota	931	            568	                61,01	            568
552062	Bílsko	    172	            119	                69,19	            119
500801	Blatec	    497	            320	                64,39	            320

   
