import mysql.connector

dbDoitProjekt = None
datenbank = "doit_projekt"

# Verbindungsaufbau zum SQL Server
try:
    dbDoitProjekt = mysql.connector.connect(
        host="localhost",
        user="weatheradm",
        password="geheim123",
        database=f"{datenbank}"
    )
    print("Verbindung zum SQL Server erfolgreich.")
except:
    mysql.connector.errors.Error("Fehler beim Verbindungsaufbau Statement!")

cursor = dbDoitProjekt.cursor()


# Erstellen des Update-Statements
def update(attribute, tabelle: str):
    sqlPlatzhalter = f"{attribute[1]}= %s"
    for i in range(2, len(attribute)):
        sqlPlatzhalter = sqlPlatzhalter + f", {attribute[i]} = %s"
    sql = f"UPDATE {datenbank}.{tabelle} " \
          f"SET {sqlPlatzhalter} " \
          f"WHERE {attribute[0]} = %s ;"
    return sql.replace("'", "").replace("[", "").replace("]", "")


# Erstellen des Insert-Statements
def insert(attribute, tabelle: str):
    sqlPlatzhalter = "%s"
    if type(attribute) == str or len(attribute) == 0:
        sql = f"INSERT INTO {datenbank}.{tabelle} " \
              f"({attribute}) " \
              f"VALUE ({sqlPlatzhalter});"
    else:
        for wert in range(len(attribute) - 1):
            sqlPlatzhalter = sqlPlatzhalter + ", %s"

        sql = f"INSERT INTO {datenbank}.{tabelle} " \
              f"({attribute}) " \
              f"VALUES ({sqlPlatzhalter});"
    return sql.replace("'", "").replace("[", "").replace("]", "")


# Datenbankabfragen vorbereiten
def select(tabelle, attribute=None):
    if attribute is None:
        sql = f"SELECT * FROM {datenbank}.{tabelle};"
    else:
        attribute: tuple

        sql = f"SELECT {attribute} FROM {datenbank}.{tabelle}".replace("[", "").replace("]", "")

    return sql.replace("\'", "")


# SQL-Statement ausführen
def executeStatement(statement, parameterListe=None):
    if type(parameterListe) == str:
        parameterListe = [parameterListe]

    try:
        cursor.execute(statement, parameterListe)
    except mysql.connector.errors.IntegrityError:
        pass
    except:
        mysql.connector.errors.Error("Fehler im Execute Statement.")


# SQL-Statement trennen
def commitStatement():
    try:
        dbDoitProjekt.commit()
    except:
        mysql.connector.errors.Error("Fehler im Commit Statement.")


# Verbindung zum SQL-Server trennen
def closeConnection():
    cursor.close()
