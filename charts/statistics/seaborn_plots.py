import csv
import matplotlib.pyplot as plt
import seaborn as sns

def wczytaj_csv(nazwa_pliku):
    data = []
    with open(nazwa_pliku) as f:
        for row in csv.reader(f):
            data.append([float(row[i]) if i == 0 else row[i]
                                          for i in range(len(row))])
    return data

def generuj_wykres_kolumnowy(dane):
    dane_do_wykresu = [item[0] for item in dane]

    plt.figure(figsize=(10, 6))
    sns.countplot(x=dane_do_wykresu)
    plt.title('Wykres kolumnowy')
    plt.xlabel('Wartości')
    plt.ylabel('Liczebność')
    plt.show()

def generuj_wykresy(nazwa_pliku):
    dane = wczytaj_csv(nazwa_pliku)
    dane_do_wykresu = [item[0] for item in dane]

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    sns.boxplot(x=dane_do_wykresu, ax=axes[0])
    axes[0].set_title('Boxplot')

    sns.histplot(dane_do_wykresu, kde=True, ax=axes[1])
    axes[1].set_title('Density Plot')

    plt.tight_layout()
    plt.show()
    
def main():
    nazwa_pliku = 'kaggle_data.csv'
    generuj_wykresy(nazwa_pliku)
    data = wczytaj_csv(nazwa_pliku)
    generuj_wykres_kolumnowy(data)
    
