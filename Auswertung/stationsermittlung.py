from geopy import distance
import sqlInterface as sql
import pandas as pd
import funktionsUndVariablensammlung as fsv

dfStationen = pd.DataFrame()
dfStationskennung = pd.DataFrame()
dfStationsMessungKennung = pd.DataFrame()
zuSuchenderOrt = None
plzDictionary = None
latlonPlz = None
distanz = "DISTANZ"
featherPfad = "stationen.feather"


# Ermittelt Breiten- und Längengrad aus einem Ortsnamen oder Postleizahl
def ermittleLatLon(ort):
    global zuSuchenderOrt, plzDictionary, latlonPlz
    zuSuchenderOrt = ort
    plzDictionary = fsv.geolocator.geocode(f"{zuSuchenderOrt}")
    latlonPlz = plzDictionary.latitude, plzDictionary.longitude
    return latlonPlz


# läd Stationsbezogene Datenbanken und erstellt daraus Dataframes
def erstelleStationenDataFrames():
    global dfStationen, dfStationskennung, dfStationsMessungKennung

    sql.executeStatement(sql.select(fsv.sqlTabelleStationen))
    dfStationen = fsv.setSpaltenNamenVonDataFrame(pd.DataFrame(sql.cursor.fetchall()), fsv.attributeStationen)

    dfStationen.index = dfStationen[fsv.attributeStationen[0]]
    del dfStationen[fsv.attributeStationen[0]]

    sql.executeStatement(sql.select(fsv.sqlTabelleStationskennung))
    dfStationskennung = fsv.setSpaltenNamenVonDataFrame(pd.DataFrame(sql.cursor.fetchall()),
                                                        fsv.attributeStationskennung)

    dfStationskennung.index = dfStationskennung[fsv.attributeStationskennung[0]]

    del dfStationskennung[fsv.attributeStationskennung[0]]

    sql.executeStatement(sql.select(fsv.sqlTabelleStationMessungKennung))
    dfStationsMessungKennung = fsv.setSpaltenNamenVonDataFrame(pd.DataFrame(sql.cursor.fetchall()),
                                                               fsv.attributeStationMessungKennung)
    dfStationsMessungKennung.index = dfStationsMessungKennung[fsv.attributeStationMessungKennung[0]]

    # Programmierfehler:
    # dfStationen[fsv.attributeStationen[0]] = dfStationen[fsv.attributeStationen[0]].astype(str)
    # Diese Zeile sollte eigentlich eingefügt werden:
    dfStationsMessungKennung[fsv.attributeStationMessungKennung[2]] = \
        dfStationsMessungKennung[fsv.attributeStationMessungKennung[2]].astype(str)

    del dfStationsMessungKennung[fsv.attributeStationMessungKennung[0]]


# Errechnet Distanz zwischen zwei GPS Koordinaten
def errechneDistanzZuPostleizahl(zeile):
    global latlonPlz
    return distance.great_circle((zeile[fsv.attributeStationen[6]], zeile[fsv.attributeStationen[7]]), latlonPlz).km


# Sortiert aufsteigend alle Stationen nach Distanz zum angegebenen ort
# und gibt nur die innerhalb des Radius zurück.
def ermittleStationenImUmkreis(ort, radius, kennung=None):
    global dfStationen, dfStationskennung, dfStationsMessungKennung, zuSuchenderOrt
    ermittleLatLon(ort)

    dfStationen[distanz] = dfStationen.apply(errechneDistanzZuPostleizahl, axis=1)

    dfGefiltert = pd.merge(pd.merge(dfStationsMessungKennung,
                                    dfStationskennung, on=fsv.attributeStationskennung[0]),
                           dfStationen, on=fsv.attributeStationskennung[1])

    dfGefiltert = dfGefiltert[(dfGefiltert[distanz] < radius)]

    dfGefiltert.sort_values(distanz, inplace=True)

    if kennung is not None:
        dfGefiltert = dfGefiltert[(dfGefiltert[fsv.attributeStationMessungKennung[1]] == kennung)]

    print(dfGefiltert)
    return dfGefiltert


# Filtert Stations Dataframe nach Kennung.
def filtereStationenNachKennung(df, kennung):
    return df[(df[fsv.attributeStationMessungKennung[1]] == kennung)]


erstelleStationenDataFrames()
