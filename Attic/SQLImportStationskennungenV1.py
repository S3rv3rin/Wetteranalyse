import sql_interface as sql

pfad = r"D:\Dev\Project_Weather\SQL_Datenbanken\statlex_rich.txt"
sqlTabelleAttributeStationskennung = ("stations_id", "stationskennung")
sqlTabelleAttributeStationMessungArt = ("id", "station_id", "stationskennung", "datum_beginn", "datum_ende")

with open(f'{pfad}', "r") as werte:
    zeilen = werte.read().split('\n')
    anzahlStationen = 0
    datensatzZaehler = 0
    for zeile in zeilen:
        anzahlStationen += 1
    print(f'Gesamt: {anzahlStationen} Datensätze')

    stationsListe = []
    fehlerListe =[]
    listengroesse = 0
    StationKennungId = 0
    for zeile in zeilen:

        StationKennungId += 1
        stationsId = zeile[40:52].replace(' ', '')
        kennungId = zeile[56:62].replace(' ', '')
        datum_beginn = f"{zeile[103:107].replace(' ', '')}-" \
                       f"{zeile[100:102].replace(' ', '')}-" \
                       f"{zeile[97:99].replace(' ', '')}"
        if datum_beginn == '--':
            datum_beginn = None
        datum_ende = f"{zeile[114:118].replace(' ', '')}-" \
                     f"{zeile[111:113].replace(' ', '')}-" \
                     f"{zeile[108:110].replace(' ', '')}"
        if datum_ende == '--':
            datum_ende = None

        MessungsArt = f"{zeile[52:56].replace(' ', '')}"

        sqlWerteStationsKennung = [kennungId, stationsId]
        sqlWerteStationMessungArt = [StationKennungId, stationsId, kennungId, datum_beginn, datum_ende]
        try:
            if kennungId not in stationsListe:
                sql.cursor.execute(sql.insert(sqlTabelleAttributeStationskennung, 'stationskennung'),
                                   sqlWerteStationsKennung)
        except:
            fehlerListe.append(sqlTabelleAttributeStationskennung)

        try:
            sql.cursor.execute(sql.insert(sqlTabelleAttributeStationMessungArt, 'station_messung_art'),
                               sqlWerteStationMessungArt)
            sql.dbDoitProjekt.commit()
            datensatzZaehler += 1
        except:
            fehlerListe.append(sqlWerteStationMessungArt)

        print(f'{datensatzZaehler} von{anzahlStationen} Datensätze abgeschlossen.')
    print(f'{len(fehlerListe)+1} Datensätze wurden nicht importiert.')
    for datensatz in fehlerListe:
        print(datensatz)