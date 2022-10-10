import sqlInterface as sql
import funktionsUndVariablensammlung as fsv

stationsLexikon = r"D:\Dev\DoIT-Projekt\SQL_Datenbanken\statlex_rich.txt"

attributeStationen = fsv.attributeStationen
attributeStationskennung = fsv.attributeStationskennung
attributeStationMessungKennung = fsv.attributeStationMessungKennung

sql.executeStatement(sql.select("stationen"))
bereitsImportierteStationen = sql.cursor.fetchall()


def ermittleOrtsDaten(filter: str):
    rückgabeWert = None
    try:
        rückgabeWert = location.raw["address"][filter]
    except:
        pass
    return rückgabeWert


with open(f"{stationsLexikon}", "r") as werte:
    zeilen = werte.read().split("\n")
    anzahlStationen = 0
    datensatzZaehler = 0
    stationsListe = []
    listengroesse = 0
    stationKennungId = 0

    for zeile in zeilen:
        anzahlStationen += 1

    print(f"Gesamt: {anzahlStationen} Datensätze")

    # Aufgrund der f Strings habe ich in der replace Funktion einfache Hochkommata. Doppelte wären mir lieber gewesen.
    abbruchbedingung = False
    for zeile in zeilen:

        if zeile == "":
            continue

        datensatzZaehler += 1
        stationKennungId += 1

        stationsId = zeile[40:52].replace(' ', '')
        for i in range(len(bereitsImportierteStationen)):
            if int(stationsId) is bereitsImportierteStationen[i][0]:
                abbruchbedingung = True
                break
        if abbruchbedingung:
            abbruchbedingung = False

            print(f"Station {stationsId} bereits importiert")
            continue

        dfStationskennung = zeile[56:62].replace(' ', '')
        kennungId = f"{zeile[52:56].replace(' ', '')}"
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

        sqlWerteStationsKennung = [dfStationskennung, stationsId]
        sqlWerteStationMessungKennung = [stationKennungId, kennungId, dfStationskennung, datum_beginn, datum_ende]

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

            sqlWerteStationen = [stationsId, zuSuchenderOrt, ort, landkreis, bundesland, land, breitengrad, laengengrad,
                                 stationshoehe]

            stationsListe.append(stationsId)

            sql.executeStatement(sql.insert(attributeStationen, "stationen"), sqlWerteStationen)

        sql.executeStatement(sql.insert(attributeStationskennung, "stationskennung"),
                             sqlWerteStationsKennung)
        sql.executeStatement(sql.insert(attributeStationMessungKennung, "stationkennung_messung_kennung"),
                             sqlWerteStationMessungKennung)
        sql.commitStatement()
        if datensatzZaehler % 100 == 0:
            print(f"{datensatzZaehler} von {anzahlStationen} Datensätze abgeschlossen.")

    print(anzahlStationen, end="\n\n")
    print(listengroesse)
