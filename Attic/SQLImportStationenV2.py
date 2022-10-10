import sqlInterface as sql
from funktionsUndVariablensammlung import ersetzen
from funktionen import locationAbrufen as lAbrufen

# Dies ist eine etwas überarbeitete Version der Datenbeschaffung/sql_import_stationen_v1.py
# Diese Version wurde verworfen, da duch das auslagern der replace Funktion und der geopy Bibliothek
# erheblich die Performance gelitten hat. Da die Version 1 erheblich schneller war, habe ich diese Version verworfen.

stationsLexikon = r"D:\Dev\DoIT-Projekt\SQL_Datenbanken\statlex_rich.txt"


attributeListe = ("stations_id", "plz", "ort", "landkreis", "bundesland",
                  "land", "breitengrad", "laengengrad", "stationshoehe")

with open(f"{stationsLexikon}", "r") as werte:
    zeilen = werte.read().split('\n')
    anzahlStationen = 0
    datensatzZaehler = 0

    for zeile in zeilen:
        print(zeile)
        anzahlStationen += 1
    print(f"Gesamt: {anzahlStationen} Datensätze")

    stationsListe = []
    listengroesse = 0

    for zeile in zeilen:
        if zeile == "":
            continue
        datensatzZaehler += 1
        stations_id = ersetzen(zeile[40:52])

        if stations_id in stationsListe:
            continue

        ort = ersetzen(zeile[0:41])
        breitengrad = ersetzen(zeile[62:71])
        laengengrad = ersetzen(zeile[71:80])
        stationshoehe = ersetzen(zeile[80:86])
        zuSuchenderOrt = lAbrufen(breitengrad, laengengrad, "address", "postcode")
        landkreis = lAbrufen(breitengrad, laengengrad, "address", "county")
        bundesland = lAbrufen(breitengrad, laengengrad, "address", "state")
        land = lAbrufen(breitengrad, laengengrad, "address", "country")

        listengroesse += 1

        sqlWerte = [stations_id, zuSuchenderOrt, ort, landkreis, bundesland, land, breitengrad, laengengrad, stationshoehe]
        stationsListe.append(stations_id)

        try:
            sql.executeStatement(sql.insert(attributeListe, "stationen"), sqlWerte)
            print(f"{datensatzZaehler} von {anzahlStationen} Datensätze abgeschlossen.")
        except:
            print(f"{stations_id} konnte nicht importiert werden.")
        try:
            sql.commitStatement()
        except:
            print("Fehler beim Commit Statement.")

    print(anzahlStationen, end="\n\n")
    print(listengroesse)
