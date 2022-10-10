import sqlInterface as sql
import pandas as pd
import funktionsUndVariablensammlung as fsv


attribute = ["stations_id", "plz"]
print(sql.select("stationen", attribute))
sql.executeStatement(sql.select("stationen", attribute))
dfStationen = fsv.setSpaltenNamenVonDataFrame(pd.DataFrame(sql.cursor.fetchall()), attribute)

print(dfStationen)

# print(sql.selectDatum(['rsk', 'tmk'], 'messungen', 'datum', '1974-09-30'))
# print(sql.selectDatum(['rsk', 'tmk'], 'messungen', 'datum', '1974-09-30', '1974-10-01'))
# ergebnisTabelle = sql.cursor.execute(sql.selectDatumZeitraum(['rsk', 'tmk'], 'messungen', 'datum', '1974-09-30'))
# ergebnisse = []


#for i in range(10):
 #   print(ergebnisse[i])


