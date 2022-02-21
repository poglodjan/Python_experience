"""
GRUPA A
Plik zawiera funkcję wczytaj_csv()
"""

def wczytaj_csv(nazwa_pliku):
    """ funkcja wczytuje dane z pliku .csv """
    data = []
    with open(nazwa_pliku) as f:
        for row in csv.reader(f):
            data.append([float(row[i]) if i == 0 else row[i]
                                          for i in range(len(row))])
    return data
