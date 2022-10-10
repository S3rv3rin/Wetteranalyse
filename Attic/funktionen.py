from geopy.geocoders import Nominatim as nm
from funktionsUndVariablensammlung import attributeMessungen as aMess
import pandas as pd
import requests
import timeit

geolocator = nm(timeout=25, user_agent="https://www.openstreetmap.org/#map")


def selectDatum(attribute, tabellen, suchattribut, erstesDatum, zweitesDatum=None):
    sql = f"SELECT {attribute} " \
          f"FROM doit_projekt.{tabellen} " \
          f"WHERE {suchattribut} "
    if zweitesDatum is None:
        sql = f"{sql} " \
              f"LIKE \"{erstesDatum}\"; "
    else:
        sql = f"{sql} " \
              f"BETWEEN \"{erstesDatum}\" AND \"{zweitesDatum}\";"

    return sql.replace("\'", "").replace("[", "").replace("]", "")

def setZeitstepmel():
    global zeitstempel
    zeitstempel = timeit.default_timer()



def listeZuQuery(liste):
    query = f"{liste[0]}"
    if len(liste) > 0:
        for i in range(1, len(liste)):
            query = f"{query},{liste[i]}"
    return query


def apiWetterAbfrage(stationen):
    return requests.get(
        f'https://dwd.api.proxy.bund.dev/v30/stationOverviewExtended?stationIds={listeZuQuery(stationen)}'). \
        content.decode()


def locationAbrufen(breitengrad, laengengrad, adress, dictFilter):
    location = geolocator.reverse(f"{breitengrad}, {laengengrad}")

    try:
        abgerufenerOrt = location.raw[adress][dictFilter]
    except:
        abgerufenerOrt = None
    return abgerufenerOrt


def konvertiereDataframeV1(dataframe):
    messwerte = dataframe.keys().tolist()
    dfsMesswert = []
    for messwert in messwerte:
        if messwert == aMess[1] or messwert == aMess[2]:
            continue

        dfMesswert = pd.DataFrame(columns=[aMess[2], messwert])
        dfMesswert[aMess[2]] = dataframe[aMess[2]]
        dfMesswert[messwert] = dataframe[messwert]
        dfsMesswert.append(dfMesswert.dropna(how="any").groupby(aMess[2], as_index=False))

    return dfsMesswert
