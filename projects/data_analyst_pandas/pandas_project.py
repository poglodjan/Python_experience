import csv

def sprawdz_poprawnosc(y):
    kolumny=len(y[0])
    krok=0
    if len(y)==0:
        print('podana lista jest pusta')
        return False
    for i in range(1,len(y)):
        if len(y[i])!=len(y[i-1]):
            print('elementy listy nie są tego samego rozmiaru')
            return False
    for wiersz in range(1,len(y)):
        for krok in range(len(y[0])):
            if type(y[wiersz][krok])!=type(y[wiersz-1][krok]):
                print('typy elementów w liście są rózne')
                return False
    return True


def wczytaj_csv(nazwa_pliku):
    data = []
    with open(nazwa_pliku) as f:
        for row in csv.reader(f):
            data.append([float(row[i]) if i == 0 else row[i]
                for i in range(len(row))])
    return data

def kategorie(y,i):
    wynik=[]
    if i!=0:
        for w in range(len(y)):
            if y[w][1]!='Female' and y[w][1]!='Male':
                wynik.append(y[w][1])
            if y[w][2]!='Yes' and y[w][2]!='No':
                wynik.append(y[w][2])
            if type(y[w][i])!=str:
                raise Exception('nie napis')
    return wynik

def grupuj(y, by):
    grupa1 = []
    grupa2 = []
    wynik=[]
    kategoria1=y[0][by]
    for w in range(len(y)):
        if y[w][by]!=kategoria1:
            kategoria2=y[w][by]
            break

    for w in range(1,len(y)):
        if y[w][by]==kategoria1:
            grupa1.append(y[w])
        if y[w][by]==kategoria2:
            grupa2.append(y[w])
    return grupa1,grupa2

def policz(y_grupy, f, i):
    wynik = []
    suma1=0
    suma2=0
    for w in range(len(y_grupy)):
        if y_grupy[w][i]=='Female':
            suma1+=1
        if y_grupy[w][i]=='Male':
            suma2+=1
    wynik.append(suma1)
    wynik.append(suma2)
    return wynik


def main():
    #sprawdzam czy macierz
    dane = wczytaj_csv('tips.csv')
    m=len(dane[0])
    for w in range(len(dane)):
        for k in range(m):
            if len(dane[k])!=len(dane[k+1]):
                print('nie macierz')
    sprawdz_poprawnosc(dane)

    for i in range(m):
        kategorie(dane,i)
    lista_unikatowych=kategorie(dane,i)
    if lista_unikatowych != []:
        print(lista_unikatowych)

    suma=0
    for w in range(len(dane)):
        suma+=dane[w][0]
    srednia_aryt=suma/len(dane)
    for i in range(len(dane[0])):
        policz(dane, 1, i)
    #grupy względem smoker
    by=2
    grupa1,grupa2=grupuj(dane,by)
    print(f'grupa1:\n {grupa1},\n \ngrupa2: \n{grupa2}')
    
    tips = wczytaj_csv("tips.csv")
    print(sprawdz_poprawnosc(tips))
    print(f'\nSrednia arytmetyczna napiwków: {srednia_aryt}')

if __name__ == '__main__':
    main()
