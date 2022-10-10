import sqlInterface
from funktionsUndVariablensammlung import attributeMessungen as aMess
import funktionsUndVariablensammlung as fsv
from Auswertung import stationsermittlung as se
from Auswertung import wetterVorraussage as wv
from Auswertung import histotischeMesswerte as hm
from Auswertung import plotting
from Datenbeschaffung import sqlImportStationenV4
from Datenbeschaffung import ftpDownloadUndUpdateMessungen
import Auswertung as aw

plz = None
ortsName = None
radius = 40
stationen = None

# Auswahlmenü für Parametereingabe für historische Messdatenanalyse
def historischesWetter():
    global plz, radius
    hm.ladeHistorischeMessungen()

    print("\nFolgende Werte können alle ausgewertet werden:\n\n"
          "Wert:        : Beschreibung:")
    for key in fsv.messungenDict:
        if key == aMess[0] or key == aMess[1] or key == aMess[2] or key == aMess[3] or key == aMess[6] or key == "T":
            continue
        leerzeichen = " "
        print(key, f"{(12 - len(key)) * leerzeichen}:", fsv.messungenDict[key][0])

    werte = str(input("\nBitte einzelne Werte durch Komma trennen:\n"
                      "Beispiel: FX,RSK,TMK\n")).upper().split(",")

    auswahlHistorischesWetter = int(input("Möchten Sie eine Datumsfilterung vornehmen?\n"
                                          "     1       = Von einem Bestimmten Datum bis heute.\n"
                                          "     2       = Ein Zeitraum zwischen zwei Daten.\n"
                                          "Alles Andere = Keine Eingränzungen.\n"))
    print("Datum bitte im Format im Format YYYY-MM-TT eingeben.")
    datum = [None, None]
    if auswahlHistorischesWetter == 2 or auswahlHistorischesWetter == 1:
        datum[0] = str(input("Startdatum = "))
    if auswahlHistorischesWetter == 2:
        datum[1] = str(input("Enddatum = "))

    auswahlZweiHistorischesWetter = input("Wie sollen die Werte der ermittelten Stationen ausgegeben werden\n"
                                          "     1       = Mittelwert\n"
                                          "     2       = Kleinster und größter Wert\n"
                                          "Alles Andere = Mittel-, kleinster und größter Wert. \n")

    plotting.erstelleGrafikenMessungen(hm.filtereMessungen(stationen, werte, datum[0], datum[1]), ortsName,
                                       auswahlZweiHistorischesWetter)

# Auswahlmenü für Wettervorhersage
def wettervorhersage():
    dictionary = wv.apiAbfrage(se.filtereStationenNachKennung(stationen, "SY"))
    dfTage = wv.konvertiereDwdApiAbfrageZuForecastTage(dictionary)
    dfForeCastStündlich = wv.konvertiereDwdApiAbfrageZuForecastStündlich(dictionary)

    auswahlWettervorhersage = int(input("Ausgabe nach Stunden oder Tagen?\n"
                                        "     1       = 48 Stunden\n"
                                        "     2       = 10 Tagen\n"
                                        "alles Andere  = Zurück.\n"))
    if auswahlWettervorhersage == 1:
        plotting.erstelleGrafikenMessungen(dfForeCastStündlich.head(48), ortsName)
    elif auswahlWettervorhersage == 2:
        plotting.erstelleGrafikenMessungen(dfTage, ortsName)
    else:
        pass


def schadstoffbelastung():
    print("Comming Soon!\n"
          "Schadstoffauswertung ist noch nicht implementiert.")

# Menü für Datenbeschaffung und Datenupdate.
def datenBeschaffungUndUpdate():
    auswahlDatenBeschaffungUndUpdate = int(input("Bitte Auswahl eingeben (Durchführung kann mehrere Stunden dauern): \n"
                                                 "1 = Update der Messungen Tabelle auf dem SQL Server.\n"
                                                 "2 = Update der Stationslisten Tabellen auf dem SQL Server.\n"
                                                 "3 = Erstelle \"messungen.feather\" Datei, \n"
                                                 "    um zukünftig schneller Auswertungen durchführen zu können.\n\n"
                                                 "Alles Andere führt zurück ins Hauptmenü!"))

    if auswahlDatenBeschaffungUndUpdate == 1:
        ftpDownloadUndUpdateMessungen.updateMessungenDatenbank()
    elif auswahlDatenBeschaffungUndUpdate == 2:
        sqlImportStationenV4.updateDatenbankenStationslisten()
    elif auswahlDatenBeschaffungUndUpdate == 3:
        aw.histotischeMesswerte.aktualisiereMessungenFeather()
    else:
        pass

# Abfrage für Ort/Region
def eingabeOrt():
    global plz, ortsName
    plz = str(input("Bitte Ortsbezeichnung oder Postleizahl der gewünschten Regioneingeben: \n"))
    ortsName = str(fsv.geolocator.geocode(plz)).split(",")

# Menü für Auswertungen
def auswertungen():
    global plz, stationen
    if plz is None:
        eingabeOrt()
    else:
        auswahlAuswertungen = int(input(f"Aktuell hinterlegter Ort ist {plz}.\n"
                                        "Möchten Sie einen neuen Ort auswerten?\n"
                                        "     1        = Ja, einen neuen Ort.\n"
                                        "alles Andere  = Nein, alter Ort weiterhin verwenden.\n"))
        if auswahlAuswertungen == 1:
            eingabeOrt()
        else:
            pass

    auswahlZweiAuswertungen = int(input("Was soll ausgewertet werden? \n"
                                        "1 = Historische Daten ab dem Jahr 1781.\n"
                                        "2 = Wettervorhersage vom Deutschen Wetterdienst.\n"
                                        "3 = Aktuelle Schadstoffbelastung\n"
                                        "Alles Andere führt zurück ins Hauptmenü!\n"))

    stationen = se.ermittleStationenImUmkreis(plz, radius)
    if auswahlZweiAuswertungen == 1:
        historischesWetter()
    elif auswahlZweiAuswertungen == 2:
        wettervorhersage()
    elif auswahlZweiAuswertungen == 3:
        schadstoffbelastung()


# Hauptmenü
print("\nWetterdaten analyse:")
while True:
    auswahl = int(input("Bitte Auswahl eingeben: \n"
                        "1 = Datenbeschaffung\n"
                        "2 = Auswertungen\n"
                        "Alles Andere lässt das Programm beenden.\n"))
    if auswahl == 1:
        datenBeschaffungUndUpdate()
    elif auswahl == 2:
        auswertungen()
    else:
        break

sqlInterface.closeConnection()
