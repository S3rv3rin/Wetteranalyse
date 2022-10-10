import pandas as pd
import requests
import funktionsUndVariablensammlung as fsv
from datetime import datetime
import json

stationen = []
zeitstempel = []
url = r"https://dwd.api.proxy.bund.dev/v30/stationOverviewExtended?stationIds="


# Erstellt URL Query aus StationsIdListe
def abfrageVorbereiten(stationsIdListe):
    stationsIdString = f"{stationsIdListe[0]}"
    if len(stationsIdListe) > 0:
        for i in range(1, len(stationsIdListe)):
            stationsIdString = f"{stationsIdString},{stationsIdListe[i]}"
    return stationsIdString


# URL Request für Wetterforecast von allen Stationen in dfStationen
def apiAbfrage(dfStationen):
    global stationen
    stationen = dfStationen[fsv.attributeStationskennung[0]].tolist()
    r = requests.get(f'{url}{abfrageVorbereiten(stationen)}').content.decode()

    return json.loads(r)


# Konvertiert Request inhalt zu einem Dataframe mit stündlichem Wetterforecast
def konvertiereDwdApiAbfrageZuForecastStündlich(dwdApiAbfrage):
    global stationen, zeitstempel
    forecaststündlich = []
    spaltenNamen = []

    for station in stationen:
        try:
            zeitstempel = int(str((dwdApiAbfrage[f"{station}"]["forecast1"]["start"]))[0:-3])
            forecaststündlich.append(dwdApiAbfrage[f"{station}"]["forecast1"]["temperature"])
            spaltenNamen.append(station)
        except:
            pass

    zeilen = []
    for i in range(241):
        messungen = []
        for einzelMessung in forecaststündlich:
            messungen.append(einzelMessung[i])

        zeilen.append([str(datetime.fromtimestamp(zeitstempel))] + messungen)

        zeitstempel += 3600
    spaltenNamen = [fsv.attributeMessungen[2]] + spaltenNamen
    dfForecastHeute = pd.DataFrame(zeilen, columns=spaltenNamen)
    dfForecastHeute = dfForecastHeute.replace([32767], None)

    dfForecastHeute.index = dfForecastHeute[spaltenNamen[0]]
    del dfForecastHeute[spaltenNamen[0]]

    maximal = round(dfForecastHeute.max(axis=1, skipna=True) / 10, 1)
    mittel = round(dfForecastHeute.mean(axis=1, skipna=True) / 10, 1)
    minimal = round(dfForecastHeute.min(axis=1, skipna=True) / 10, 1)

    dfConcat = pd.concat([maximal, mittel, minimal], axis=1)
    dfConcat.columns = ["T-Maximal", "T-Mittelwert", "T-Minimal"]
    return dfConcat


# Konvertiert Request inhalt zu einem Dataframe mit täglichen Wetterforecast
def konvertiereDwdApiAbfrageZuForecastTage(dwdApiAbfrage):
    global stationen
    forecastTage = []
    spaltenNamen = [fsv.attributeMessungen[2], "TMK-Maximal", "TMK", "TMK-Minimal", "RSK",
                    "FX"]

    for station in stationen:
        try:
            for day in dwdApiAbfrage[f"{station}"]["days"]:
                forecastTage.append((day["dayDate"], day["temperatureMax"], None, day["temperatureMin"],
                                     day["precipitation"], day["windSpeed"]))
        except:
            pass
    dfForecastTage = pd.DataFrame(forecastTage, columns=spaltenNamen)
    dfForecastTage[spaltenNamen[2]] = (dfForecastTage[spaltenNamen[1]] + dfForecastTage[spaltenNamen[3]]) / 2
    del dfForecastTage[spaltenNamen[1]]
    del dfForecastTage[spaltenNamen[3]]

    return fsv.konvertiereDataframe(dfForecastTage)
