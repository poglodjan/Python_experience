import csv

def wczytaj_csv():
    uczestnicy = []
    with open("wyniki_ankiety.csv") as f:
        for row in csv.reader(f):
            uczestnicy.append(row)
    return uczestnicy

def zlicz_odpowiedzi(macierz):
    C=[ [0]*5 for i in range(3)]
    n=len(macierz)
    m=len(macierz[0])
    pytanie=0
    for w in range(n):
        for k in range(3,m):
            if macierz[w][k]=='tak':
                C[0][pytanie]+=1
            if macierz[w][k]=='nie':
                C[1][pytanie]+=1
            if macierz[w][k]=='b/o':
                C[2][pytanie]+=1
            pytanie+=1
        pytanie=0
    return C

def statystyki(macierz):
    liczba_ankietowanych=len(macierz)
    srednia_wieku=0
    liczba_kobiet=0
    liczba_mężczyzn=0
    wiek=0
    for w in range(liczba_ankietowanych):
        if int(macierz[w][2]!='' ):
            wiek+=int(macierz[w][2])
        else: liczba_ankietowanych-=1
        if macierz[w][1]=='k':
            liczba_kobiet+=1
        if macierz[w][1]=='m':
            liczba_mężczyzn+=1

        srednia_wieku=wiek/liczba_ankietowanych

    return srednia_wieku, liczba_mężczyzn, liczba_kobiet, liczba_ankietowanych


def narysuj_tabele(zliczenie):
    print('             TAK NIE b/o')
    print('-------------------------')
    for w in range(len(zliczenie[0])):
        print(f'Pytanie {w}     {zliczenie[0][w]}  {zliczenie[1][w]}  {zliczenie[2][w]}')
        print('-------------------------')
        

def main():
    macierz=wczytaj_csv()
    C=zlicz_odpowiedzi(macierz)
    narysuj_tabele(C)
    print(C)

    srednia_wieku, liczba_mężczyzn, liczba_kobiet, liczba_ankietowanych=statystyki(macierz)
    print(round(srednia_wieku,1), liczba_mężczyzn, liczba_kobiet, liczba_ankietowanych)

if __name__ == '__main__':
    main()
