import matplotlib.pyplot as plt
import funktionsUndVariablensammlung as fsv

# Erstellt für jeden Messwert eine eigene Grafik:
def erstelleGrafikenMessungen(df, ort, auswahl=None):
    spalten = [str(spalte) for spalte in df.keys().tolist()]
    if spalten[0] == fsv.attributeMessungen[2]:
        del df[spalten[0]]
    for i in range(0, len(spalten), 3):

        messung = fsv.messungenDict[spalten[i].split("-")[0]]

        title = f"{messung[0]} im Umkreis von {ort[-2]} {ort[0]}"

        # Mittelwert
        if auswahl == 1:
            df.plot(y=[df.columns[i + 1]], rot="15", ylabel=messung[1], grid=True, title=title)
        # Minimal und Maximal
        elif auswahl == 2:
            df.plot(y=[df.columns[i], df.columns[i + 2]], rot="15", ylabel=messung[1], grid=True, title=title)
        # alle
        else:
            df.plot(y=[df.columns[i], df.columns[i + 1], df.columns[i + 2]], rot="15", ylabel=messung[1], grid=True,
                    title=title)
    plt.show()
