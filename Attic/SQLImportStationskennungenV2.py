import sqlInterface as sql
from funktionen import ersetzen
import funktionsUndVariablensammlung as fsv

stationslexikon = r"D:\Dev\DoIT-Projekt\SQL_Datenbanken\statlex_rich.txt"


with open(f"{stationslexikon}", "r") as werte:
    zeilen = werte.read().split("\n")
    anzahlStationen = 0
    datensatzZaehler = 0
    for zeile in zeilen:
        anzahlStationen += 1
    print(f"Gesamt: {anzahlStationen} Datensätze")

    stationsListe = []
    fehlerListe = []
    listengroesse = 0
    StationKennungId = 0
    for zeile in zeilen:

        StationKennungId += 1
        stationsId = ersetzen(zeile[40:52])
        kennungId = ersetzen(zeile[56:62])
        datum_beginn = f"{ersetzen(zeile[103:107])}" \
                       f"{ersetzen(zeile[100:102])}-" \
                       f"{ersetzen(zeile[97:99])}"
        if datum_beginn == '--':
            datum_beginn = None
        datum_ende = f"{ersetzen(zeile[114:118])}-" \
                     f"{ersetzen(zeile[111:113])}-" \
                     f"{ersetzen(zeile[108:110])}"
        if datum_ende == "--":
            datum_ende = None

        MessungsArt = f"{ersetzen(zeile[52:56])}"

        sqlWerteStationsKennung = [kennungId, stationsId]
        sqlWerteStationMessungArt = [StationKennungId, stationsId, kennungId, datum_beginn, datum_ende]

        if kennungId not in stationsListe:
            sql.executeStatement(sql.insert(fsv.sqlTabelleAttributeStationskennung, "stationskennung"),
                                 sqlWerteStationsKennung)

        sql.executeStatement(sql.insert(fsv.sqlTabelleAttributeStationMessungArt, "station_messung_art"),
                             sqlWerteStationMessungArt)

        print(f"{datensatzZaehler} von {anzahlStationen} Datensätze abgeschlossen.")
    sql.commitStatement()
    print(f"{len(fehlerListe) + 1} Datensätze wurden nicht importiert.")
    for datensatz in fehlerListe:
        print(datensatz)
