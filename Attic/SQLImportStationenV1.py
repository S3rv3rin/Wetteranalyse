from geopy.geocoders import Nominatim as nm
import sqlInterface as sql

geolocator = nm(user_agent="https://www.openstreetmap.org/#map")

pfad = r"D:\Dev\Project_Weather\SQL_Datenbanken\statlex_rich.txt"
attributeListe = ("stations_id", "plz", "ort", "landkreis", "bundesland",
                  "land", "breitengrad", "laengengrad", "stationshoehe")

with open(f'{pfad}', "r") as werte:
    zeilen = werte.read().split('\n')
    anzahlStationen = 0
    datensatzZaehler = 0
    for zeile in zeilen:
        anzahlStationen += 1
    print(f'Gesamt: {anzahlStationen} Datensätze')

    stationsListe = []
    listengroesse = 0
    for zeile in zeilen:

        if zeile == '':
            continue
        datensatzZaehler += 1
        stations_id = zeile[40:52].replace(' ', '')

        if stations_id in stationsListe:
            continue

        ort = zeile[0:41].replace('  ', '')
        breitengrad = zeile[62:71].replace(' ', '')
        laengengrad = zeile[71:80].replace(' ', '')
        stationshoehe = zeile[80:86].replace(' ', '')

        location = geolocator.reverse(f"{breitengrad}, {laengengrad}")

        try:
            zuSuchenderOrt = location.raw['address']['postcode']
        except:
            pass

        try:
            landkreis = location.raw['address']['county']
        except:
            pass
        try:
            bundesland = location.raw['address']['state']
        except:
            pass
        try:
            land = location.raw['address']['country']
        except:
            pass
        listengroesse += 1

        sqlWerte = [stations_id, zuSuchenderOrt, ort, landkreis, bundesland, land, breitengrad, laengengrad, stationshoehe]
        stationsListe.append(stations_id)

        try:
            sql.cursor.execute(sql.insert(attributeListe, 'stationen'), sqlWerte)
            sql.dbDoitProjekt.commit()
            print(f'{datensatzZaehler} von{anzahlStationen} Datensätze abgeschlossen.')
        except:
            print(f'{stations_id} konnte nicht importiert werden.')

    print(anzahlStationen, end="\n\n")
    print(listengroesse)

