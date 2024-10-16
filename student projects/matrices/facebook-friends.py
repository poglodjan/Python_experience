import random
import math
import matplotlib.pyplot as plt

def macierz_startowa(n):
    A=[ [0]*n for i in range(n)]
    for wiersz in range(len(A)):
        for kolumna in range(len(A[0])):
            if wiersz!=kolumna:
                A[wiersz][kolumna]=1
    return A

def licznosc_stopni(A):
    popularnosc_wiersze=[0]*len(A) #pomocnicza tablica liczaca popularnosc
    popularnosc_kolumny=[0]*len(A[0])
    krokwiersze=0
    krokkolumny=0
    for w in range(len(A)):
        if A[w][0]==1:
            popularnosc_wiersze[krokwiersze]+=1
        if A[w][1]==1:
            popularnosc_wiersze[krokwiersze]+=1
        if A[w][2]==1:
            popularnosc_wiersze[krokwiersze]+=1
        if A[w][3]==1:
            popularnosc_wiersze[krokwiersze]+=1
        #sprawdzam w kolumnach:
        for k in range(len(A[0])):
            if A[w][k]==1:
                popularnosc_kolumny[krokkolumny]+=1
            krokkolumny+=1
        krokkolumny=0
        krokwiersze+=1
    #szukam najwiekszej popularnosci
    max_popularnosc_kolumny=max(popularnosc_kolumny)
    max_popularnosc_wiersz=max(popularnosc_wiersze)
    max_popul=max(max_popularnosc_kolumny, max_popularnosc_wiersz)
    l=[0]*(max_popul+1)

    dl=len(popularnosc_wiersze) #=popularnosc_kolumny
    for i in range(dl):
        for j in range(dl):
            if i==popularnosc_kolumny[j] and i==popularnosc_wiersze[j]: #ta koniunkcja i tak jest zawsze bo a[i,j] zna a[j,i]
                l[i]+=1
    return l

def nowe_grono(A, N, m):
    if m<0: #sprawdzamy błędy
        raise ValueError('m powinno być dodatnie')
    if m>=len(A):
        raise ValueError('m powinno być mniejsze od poprzedniej liczby osob')
    if len(A)>N:
        raise ValueError('liczba nowego grona powinna byc wieksza od starego')

    B=[ [0]*N for i in range(N)]
    for w in range(len(A)): #wstawiamy dane znajomosci z poprzedniej macierzy
        for k in range(len(A[0])):
            B[w][k]=A[w][k]
    a=len(A)
    b=len(B)
    lista=[ i for i in range(b)]

    for krok in range(b-a): #krok to każda nowa osoba

        losowo_wybrani = random.sample(lista, m)
        print(losowo_wybrani)
        for w in range(b):
            for k in range(b):    
                c=losowo_wybrani[0]
                d=losowo_wybrani[1]
                if w!=k:
                   B[c][d]=1
                   B[d][c]=1  #ustawiamy też symetrycznie    
    return B

def p(k, m):
    if k==0:
        return 0
    licznik = math.exp(1- (m/k))
    ulamek=licznik/m
    if k<m:
        return 0
    else:
        return ulamek

def srednie_bledy(T,A):
    m=5
    v=[0]*100
    N=100
    suma=0
    for i in range(N):
        suma=0
        for t in range(T):
            y=nowe_grono(A,5,3)
            k=licznosc_stopni(A)
            suma+=k-(100*p(i,m))
        v[i] = suma/T
    return v

def main():
    A = macierz_startowa(4)
    l = licznosc_stopni(A)
    for row in A:
        print(row)
    print('_____________')
    print(l)
    B = nowe_grono(A, 6, 2)
    print('_____________')
    for row in B:
        print(row)

    sb = srednie_bledy(1000,A)
    print(sb[:5])

    #plt.scatter(x, y)
    #plt.show()

if __name__ == '__main__':
    main()
