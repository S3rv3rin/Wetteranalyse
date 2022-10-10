import zipfile
from ftplib import FTP
import sqlInterface as sql
import os
import funktionsUndVariablensammlung as fsv
from funktionsUndVariablensammlung import attributeMessungen as aMess

host = "opendata.dwd.de"
pfad = "climate_environment/CDC/observations_germany/climate/daily/kl/historical/"
benutzer = ""
passwort = ""

# Datenbankabfrage der bereits importierten Dateien:
# zurückgegebener Datentyp = Tuple
sql.executeStatement(sql.select(fsv.sqlTabelleFtpDateien))
bereitsImportierteArchive = sql.cursor.fetchall()


# Bereitet die Zeilen für den SQL-Insert vor und führt diesen durch.
def messungenImportieren(zeilen):
    datensatzZaehler = 1

    # Formatieren der Zeile und konvertieren der "None"-Werte
    for i in range(1, len(zeilen)):
        zeile = zeilen[i].replace(" ", "").replace(";", ",").replace("\n", "").split(",")
        if zeile == ['']:
            continue
        for ii in range(len(zeile)):
            if zeile[ii] == "-999":
                zeile[ii] = None

        sqlWerte = [f"{zeile[1]}-{zeile[0]}"] + zeile

        sql.executeStatement(sql.insert(attribute=aMess, tabelle=aMess), sqlWerte)

        datensatzZaehler += 1

    sql.commitStatement()
    print(f"{datensatzZaehler} Datensätze wurden importiert. ")

    return datensatzZaehler

# Download der Messungen,
def updateMessungenDatenbank():
    with FTP(host) as ftp:
        try:
            ftp.login(user=benutzer, passwd=passwort)
            print(ftp.getwelcome())
        except:
            print('Problem beim Verbindungsaufbau zum FTP Server.')

        # Öffnen des Pfades auf dem Server
        ftp.cwd(pfad)
        dateinamen = ftp.nlst()

        archivpfad = "archiv"
        dateienZähler = 0
        datensatzZähler = 0
        abbruchbedingung = False

        for dateiname in dateinamen:
            if not ".zip" in dateiname:
                continue

            for i in range(len(bereitsImportierteArchive)):
                if dateiname == bereitsImportierteArchive[i][0]:
                    abbruchbedingung = True
                    break
            if abbruchbedingung:
                abbruchbedingung = False
                continue

            # Download der Dateien vom FTP Server
            with open(dateiname, "wb") as datei:
                if os.path.isfile(dateiname):
                    ftp.retrbinary("RETR %s" % dateiname, datei.write)

            # Archiv öffnen
            with zipfile.ZipFile(dateiname) as archiv:
                archivdateien = archiv.namelist()
                wertedatei = None

                # Namesermittlung der "produkt_klima_*.txt"
                for index in range(len(archivdateien)):
                    if "produkt_klima" in archivdateien[index]:
                        wertedatei = archivdateien[index]

                        # Entpacken
                        archiv.extract(f"{wertedatei}", archivpfad)

                        with open(f"{archivpfad}\\{wertedatei}") as entpacktesArchiv:
                            werte = entpacktesArchiv.read().split(";eor")

                            # Datenbankimport
                            datensatzZähler += messungenImportieren(werte)

            sql.executeStatement(sql.insert(fsv.attributeFtpDateien[0], fsv.sqlTabelleFtpDateien), dateiname)

            sql.commitStatement()

            os.remove(f"archiv/{wertedatei}")
            os.remove(dateiname)

            print(f"{datensatzZähler} Datensätze wurden importiert. ")
            dateienZähler += 1
        for datei in os.listdir():
            if datei == "archiv":
                os.rmdir("archiv")
