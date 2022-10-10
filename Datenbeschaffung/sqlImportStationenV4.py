import sqlInterface as sql
import funktionsUndVariablensammlung as fsv
import requests
import os

downloadURL = r"https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_rich.txt?view=" \
              r"nasPublication&nn=16102"
stationsLexikon = requests.get(downloadURL, timeout=25)
statLex = "statLex.txt"

sql.executeStatement(sql.select(fsv.sqlTabelleStationen))
bereitsImportierteStationen = sql.cursor.fetchall()

sql.executeStatement(sql.select(fsv.sqlTabelleStationMessungKennung))
bereitsImportierteStationskennungMessungKennung = sql.cursor.fetchall()

location = None

# Gibt aus dem Dictionary "location" den entsprechenden String der Adresse zurück.
def ermittleOrtsDaten(filter: str):
    global location
    rückgabeWert = None
    try:
        rückgabeWert = location.raw["address"][filter]
    except:
        pass
    return rückgabeWert

# Download, update und insert des Stationslexikons
def updateDatenbankenStationslisten():
    global location

    # Download
    with open(statLex, "wb") as datei:
        datei.write(stationsLexikon.content)


    with open(statLex, "r") as werte:
        zeilen = werte.read().split("\n")
        anzahlStationen = 0
        datensatzZaehler = 0
        stationsListe = []
        listengroesse = 0
        stationKennungId = 0

        for zeile in zeilen:
            anzahlStationen += 1
        print(f"Gesamt: {anzahlStationen} Datensätze")

        # Auslesen der Stationsdaten aus dem Stationslexikon.
        # Aufgrund der f-Strings wurden in der replace Funktion einfache
        # Hochkommata verwendet, Doppelte wären einheitlicher gewesen.
        abbruchbedingung = False
        for zeile in zeilen:
            if zeile is zeilen[0] or zeile is zeilen[1] or zeile is zeilen[2]:
                continue
            if zeile == "":
                continue

            datensatzZaehler += 1
            stationKennungId += 1
            kennungId = f"{zeile[52:56].replace(' ', '')}"
            stationsId = zeile[40:52].replace(' ', '')
            stationskennung = zeile[56:62].replace(' ', '')
            datum_beginn = f"{zeile[103:107].replace(' ', '')}-" \
                           f"{zeile[100:102].replace(' ', '')}-" \
                           f"{zeile[97:99].replace(' ', '')}"
            if datum_beginn == '--':
                datum_beginn = None
            datum_ende = f"{zeile[114:118].replace(' ', '')}-" \
                         f"{zeile[111:113].replace(' ', '')}-" \
                         f"{zeile[108:110].replace(' ', '')}"
            if datum_ende == "--":
                datum_ende = None

            # Update bereits importierter Zeilen
            for i in range(len(bereitsImportierteStationskennungMessungKennung)):
                if stationskennung is bereitsImportierteStationskennungMessungKennung[i][2]:
                    abbruchbedingung = True
                    sql.executeStatement(
                        sql.update(fsv.attributeStationMessungKennung, fsv.sqlTabelleStationMessungKennung),
                        [kennungId, stationskennung, datum_beginn, datum_ende, stationKennungId])
                    break
            for i in range(len(bereitsImportierteStationen)):
                if int(stationsId) is bereitsImportierteStationen[i][0]:
                    abbruchbedingung = True
                    break
            if abbruchbedingung:
                abbruchbedingung = False

                print(f"Station {stationsId} bereits importiert")
                continue

            kennungId = f"{zeile[52:56].replace(' ', '')}"

            sqlWerteStationsKennung = [stationskennung, stationsId]
            sqlWerteStationMessungKennung = [stationKennungId, kennungId, stationskennung, datum_beginn, datum_ende]

            # Fertigstellen der sql Werte und Insert in jeweilige Tabelle
            if stationsId not in stationsListe:
                ort = zeile[0:41].replace(' ', '')
                breitengrad = zeile[62:71].replace(' ', '')
                laengengrad = zeile[71:80].replace(' ', '')
                stationshoehe = zeile[80:86].replace(' ', '')

                location = fsv.geolocator.reverse(f"{breitengrad}, {laengengrad}")

                zuSuchenderOrt = ermittleOrtsDaten("postcode")
                landkreis = ermittleOrtsDaten("county")
                bundesland = ermittleOrtsDaten("state")
                land = ermittleOrtsDaten("country")

                listengroesse += 1

                sqlWerteStationen = [stationsId, zuSuchenderOrt, ort, landkreis, bundesland, land, breitengrad,
                                     laengengrad,
                                     stationshoehe]

                stationsListe.append(stationsId)

                sql.executeStatement(sql.insert(fsv.attributeStationen, fsv.sqlTabelleStationen), sqlWerteStationen)

            sql.executeStatement(sql.insert(fsv.attributeStationskennung, fsv.sqlTabelleStationskennung),
                                 sqlWerteStationsKennung)
            sql.executeStatement(sql.insert(fsv.attributeStationMessungKennung, fsv.sqlTabelleStationMessungKennung),
                                 sqlWerteStationMessungKennung)
            sql.commitStatement()
            if datensatzZaehler % 100 == 0:
                print(f"{datensatzZaehler} von {anzahlStationen} Datensätze abgeschlossen.")
        print(anzahlStationen, end="\n\n")
        print(listengroesse)
    os.remove(statLex.txt)
