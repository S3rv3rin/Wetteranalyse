from datetime import date
import sqlInterface as sql
import pandas as pd
import funktionsUndVariablensammlung as fsv
from funktionsUndVariablensammlung import attributeMessungen as aMess

pfad = r"Auswertung/messungen.feather"
dfMessungen = pd.DataFrame()


# Erstellt ein Dataframe aus SQL Abfrage
def erstelleMessungenDataFrames():
    global dfMessungen
    sql.executeStatement(sql.select(fsv.sqlTabelleMessungen))
    dfMessungen = fsv.setSpaltenNamenVonDataFrame(pd.DataFrame(sql.cursor.fetchall()), aMess)


# Erstellt ein Dataframe und sichert es als feather Datei
def aktualisiereMessungenFeather():
    erstelleMessungenDataFrames()
    fsv.speichereFeather(dfMessungen, pfad)


# Filtert dfMessungen nach angegebenen Parametern
def filtereMessungen(stationen, messwerte, datumBeginn=None, datumEnde=None):
    global dfMessungen
    if datumBeginn is not None:
        datumBeginn = fsv.datumZuJahrMonatTag(datumBeginn)
    if datumEnde is not None:
        datumEnde = fsv.datumZuJahrMonatTag(datumEnde)

    spaltenNamen = [aMess[1], aMess[2]] + messwerte
    stationen = [int(station) for station in list(dict.fromkeys(stationen[aMess[1]].tolist()))]
    dfGefiltert = dfMessungen[spaltenNamen]
    if datumBeginn is not None:
        if datumEnde is not None:
            dfGefiltert = dfGefiltert[(dfGefiltert[aMess[1]].isin(stationen)) &
                                      (dfGefiltert[aMess[2]] >=
                                       date(datumBeginn[0], datumBeginn[1], datumBeginn[2])) &
                                      (dfGefiltert[aMess[2]] <=
                                       date(datumEnde[0], datumEnde[1], datumEnde[2]))]
        else:
            dfGefiltert = dfGefiltert[(dfGefiltert[aMess[1]].isin(stationen)) &
                                      (dfGefiltert[aMess[2]] >=
                                       date(datumBeginn[0], datumBeginn[1], datumBeginn[2]))]
    else:
        dfGefiltert = dfGefiltert[(dfGefiltert[aMess[1]].isin(stationen))]
    print("\n\n",dfGefiltert,"\n")
    return fsv.konvertiereDataframe(dfGefiltert)


# Läd Messungen vorrangig aus Feather Datei und alternativ von SQL Server
def ladeHistorischeMessungen():
    global dfMessungen, pfad
    try:
        print("Importiere Messungen von Feather Datei zu importieren.")
        dfMessungen = fsv.leseFeather(pfad)

        print(f"Dataframe von messungen.feather wurde importiert.")

    except:
        print("Keine Feather Datei vorhanden. Daten werden vom SQL Server importiert.")
        aktualisiereMessungenFeather()
        print(f"Dataframe wurde vom SQL Server importiert.")
