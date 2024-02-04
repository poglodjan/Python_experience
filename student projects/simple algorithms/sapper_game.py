import random

def wypisz_macierz(matrix):
    print(" ", end=" ")
    for column in range(len(matrix[0])):
        if column < 10:
            print(column, end=" ")
        else:
            print(chr(ord("A")+column-10), end=" ")
    print()

    for row in range(len(matrix)):
        if row < 10:
            print(row, end=" ")
        else:
            print(chr(ord("A")+row-10), end=" ")
        for column in range(len(matrix[row])):
            print(f"{matrix[row][column]}", end=" ")
        print()
    print()

def losuj_miny(plansza, liczba_min):
    b=liczba_min
    for i in range(b):
        x=random.randint(0,9)
        y=random.randint(0,14)
        if plansza[x][y]==0:
            plansza[x][y]=9
        elif plansza[x][y]==9:
            x=random.randint(0,9)
            y=random.randint(0,14)
            if plansza[x][y]==0:
                plansza[x][y]=9
            else: b+=1
    return plansza

def wypisz_macierz_cenzura(plansza, cenzura,C):
    for w in range(len(plansza)):
        for k in range(len(plansza[0])):
            if cenzura[w][k]==True:
                C[w][k]=plansza[w][k]
            elif cenzura[w][k]==False: 
                C[w][k]='*'        
    wypisz_macierz(C)

def odkryj_pole(plansza, cenzura, wiersz, kolumna):
    if wiersz>len(plansza):
        return False
    if kolumna>len(plansza[0]):
        return False
    if plansza[wiersz][kolumna]==9:
        return False
    elif plansza[wiersz][kolumna]!=9:
        cenzura[wiersz][kolumna]=True
        return True

def numery_przy_minach(plansza):
    for w in range(len(plansza)):
        for k in range(len(plansza[0])):
            if plansza[w][k]!=9 and (w>0 and k>0) and (w<9 and k<14):
                if plansza[w-1][k]==9:
                    plansza[w][k]+=1
                if plansza[w-1][k-1]==9:
                    plansza[w][k]+=1
                if plansza[w][k-1]==9:
                    plansza[w][k]+=1
                if plansza[w+1][k]==9:
                    plansza[w][k]+=1
                if plansza[w+1][k+1]==9:
                    plansza[w][k]+=1
                if plansza[w][k+1]==9:
                    plansza[w][k]+=1
            if plansza[w][k]!=9 and w==0:
                if plansza[w-1][k]==9:
                    plansza[w][k]+=1
                if plansza[w][k]==9:
                    plansza[w-1][k+1]+=1
                if plansza[w+1][k]==9:
                    plansza[w][k]+=1
    return plansza


def main():
    plansza = [[0]*15 for i in range(10)]
    cenzura = [[False]*15 for i in range(10)]
    C=[[0]*15 for i in range(10)]
    n=len(plansza)
    m=len(plansza[0])

    plansza=losuj_miny(plansza, liczba_min=15)
    wypisz_macierz(plansza)
    wypisz_macierz_cenzura(plansza,cenzura,C)
    plansza=numery_przy_minach(plansza)
    wypisz_macierz(plansza)

    for i in range(5):
        wiersz=int(input('wczytaj wiersz'))
        kolumna=int(input('wczytaj kolumne'))
        if odkryj_pole(plansza, cenzura, wiersz, kolumna)==False:
            print('przegrałeś!')
            return 0
        elif odkryj_pole(plansza, cenzura, wiersz, kolumna)==True:
            wypisz_macierz_cenzura(plansza,cenzura,C)        
            continue


if __name__ == '__main__':
    main()
