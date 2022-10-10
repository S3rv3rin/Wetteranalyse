from geopy.geocoders import Nominatim as nm
import pandas as pd

geolocator = nm(timeout=25, user_agent="https://www.openstreetmap.org/#map")

# Print(DataFrame) gibt bei diesen Optionen alle Zeilen oder Spalten aus.
# pd.set_option("display.max_column", None)
# pd.set_option("display.max_rows", None)


# Designfehler alle Variablen sind public und nicht immutable:
sqlTabelleFtpDateien = "ftp_dateien"


# Lösungsansatz:
def getSqlTabelleFtpDateien():
    return "ftp_dateien"


attributeFtpDateien = ["DATEINAMEN"]

sqlTabelleStationskennung = "stationskennung"
attributeStationskennung = ["STATIONSKENNUNG", "STATIONS_ID"]

sqlTabelleStationMessungKennung = "stationkennung_messung_kennung"
attributeStationMessungKennung = ["ID", "KENNUNG_ID", "STATIONSKENNUNG", "DATUM_BEGINN", "DATUM_ENDE"]

sqlTabelleMessungen = "messungen"
attributeMessungen = ["MESSUNG_ID", "STATIONS_ID", "MESS_DATUM", "QN_3", "FX", "FN", "QN_4", "RSK", "RSKF", "SDK",
                      "SHK_TAG",
                      "NM", "VPM", "PM", "TMK", "UPM", "TXK", "TNK", "TGK"]
sqlTabelleStationen = "stationen"
attributeStationen = ["STATIONS_ID", "PLZ", "ORT", "LANDKREIS", "BUNDESLAND", "LAND", "BREITENGRAD", "LAENGENGRAD",
                      "STATIONSHOEHE"]


messungenDict = {attributeMessungen[0]: ["Messungs ID"],
                 attributeMessungen[1]: ["Stationsidentifikationsnummer"],
                 attributeMessungen[2]: ["Datum/ Zeitpunkt"],
                 attributeMessungen[3]: ["Qualitätsniveau der nachfolgenden Spalte"],
                 attributeMessungen[4]: ["Tagesmaximum Windspitze", "m/s"],
                 attributeMessungen[5]: ["Tagesmittel Windgeschwindigkeit", "m/s"],
                 attributeMessungen[6]: ["Qualitätsniveau der nachfolgenden Spalten"],
                 attributeMessungen[7]: ["Tägliche Niederschlagshöhe", "mm"],
                 attributeMessungen[8]: ["Niederschlagsform"],
                 attributeMessungen[9]: ["Tägliche Sonnenscheindauer", "Stunden"],
                 attributeMessungen[10]: ["Tageswert Schneehöhe", "cm"],
                 attributeMessungen[11]: ["Tagesmittel des Bedeckungsgrades"],
                 attributeMessungen[12]: ["Tagesmittel des Dampfdruckes", "hPa"],
                 attributeMessungen[13]: ["Tagesmittel des Luftdrucks", "hPa"],
                 attributeMessungen[14]: ["Tagesmittel der Temperatur", "°C"],
                 attributeMessungen[15]: ["Tagesmittel der Relativen Feuchte", "%"],
                 attributeMessungen[16]: ["Tagesmaximum der Lufttemperatur in 2m Höhe", "°C"],
                 attributeMessungen[17]: ["Tagesminimum der Lufttemperatur in 2m Höhe", "°C"],
                 attributeMessungen[18]: ["Minimum der Lufttemperatur am Erdboden in 5cm Höhe", "°C"],
                 "T": ["Temperaturen", "°C"]
                 }


# Sucht und ersetzt Zeichen in einem String
def ersetzen(abschnitt: str):
    return abschnitt.replace(" ", "").replace(";", ",").replace("\n", "")


# Nennt spaltennamen des Dataframes um
def setSpaltenNamenVonDataFrame(df: pd.DataFrame, liste):
    keys = []
    for i in range(len(liste)):
        keys.append([i, liste[i]])
    keys = dict(keys)
    df.rename(keys, axis=1, inplace=True)
    return df


# Konvertiert Datumsstring von "yyyy-mm-tt" zu einer Liste mit Integern [jahr, monat, tag]
def datumZuJahrMonatTag(datumUnformatiert: str):
    return [int(datumUnformatiert[0:4]), int(datumUnformatiert[5:7]), int(datumUnformatiert[8:10])]


# Gruppiert ein Dataframe nach Messdatum.
# Für jedes Datum wird Minimal, Maximal und Mittelwert ermittelt
# und wieder zu einem Dataframe verbunden#
def konvertiereDataframe(dataframe: pd.DataFrame):
    messwerte = dataframe.keys().tolist()
    del messwerte[0]
    for spalte in dataframe.columns:
        if attributeMessungen[1] in spalte:
            del dataframe[spalte]

    dfGruppiert = dataframe.groupby(attributeMessungen[2])
    mittel = dfGruppiert.mean()
    minimal = dfGruppiert.max()
    maximal = dfGruppiert.min()

    # print("\nMittelwert:\n",mittel.head(5))
    # print("\nKleinster Wert:\n", minimal.head(5))
    # print("\nGrößter Wert:\n", maximal.head(5))

    dfMerged = pd.merge(pd.merge(mittel, minimal, on=attributeMessungen[2]), maximal, on=attributeMessungen[2])
    print(dfMerged.head(5))
    dfMerged.sort_index(axis=1, inplace=True)
    spaltenNamen = dfMerged.keys().tolist()
    spaltensuffix = ["-Maximal", "-Mittelwert", "-Minimal"]
    for messwert in messwerte:
        counter = 0
        for i in range(len(spaltenNamen)):
            if messwert in spaltenNamen[i]:
                spaltenNamen[i] = f"{messwert}{spaltensuffix[counter]}"
                counter += 1
            if counter == 3:
                break
    dfMerged.columns = spaltenNamen
    return dfMerged


# Speichert Dataframe als Feather Datei
def speichereFeather(df: pd.DataFrame, pfad: str):
    df.to_feather(pfad)


# Liest Dataframe aus Feather Datei
def leseFeather(pfad: str):
    df = pd.read_feather(pfad)
    return df
