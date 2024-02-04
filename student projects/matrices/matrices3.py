import random

def wypisz_macierz(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if type(matrix[row][column]) is float:
                print(f'{matrix[row][column]:6.2}', end=" ")
            else:
                print(f'{matrix[row][column]:6}', end=" ")
        print()
    print()

def losuj_macierz(wiersze, kolumny, a, b):
    return [[random.randint(a, b) for j in range(kolumny)] for i in range(wiersze)]

def losuj_wektor(n, a, b):
    return [random.randint(a, b) for j in range(n)]

def mnoz_macierz_wektor(A, b):
    wierszeA=len(A)
    kolumnyA=len(A[0])
    dl_wek=len(b)
    wynik=[0] * wierszeA

    if kolumnyA!=dl_wek:
        raise ValueError('niepoprawne dane, aby wykonać mnozenie') 

    for w in range(wierszeA):
        for k in range(kolumnyA):
            pom=A[w][k]*b[k]
            wynik[w]+=pom
    return wynik

def macierz_vandermonde(alfa, n):
    m=len(alfa)
    gasienica=0
    pom=1
    M=[ [1]*n for i in range(m) ]
    for w in range(m):
        for k in range(1,n):
            pom*=alfa[gasienica]
            M[w][k]*=pom
        gasienica+=1
        pom=1
    return M

def czy_macierz_permutacji(A):
    n=len(A)
    m=len(A[0])
    ilosc1=0
    p=1
    if m!=n:
        return False
    for i in range(n):
        for j in range(m):
            if A[i][j]==0 or A[i][j]==1:
                continue
            else: return False
    for i in range(n):
        for j in range(m):
            if A[i][j]==1:
                ilosc1+=1
                if ilosc1>1: 
                    p=0
        ilosc1=0
    if p==0: return False
    else: return True

def main():
    random.seed(123)
    a=0
    b=4
    w=3
    k=4

    A=losuj_macierz(w,k,a,b)
    n=len(A[0])
    wek=losuj_wektor(n,a,b)
    
    print(f'wylosowana macierz: {A}')
    print(f'wylosowany wektor: {wek}')
    C=mnoz_macierz_wektor(A,wek)
    print(f'iloczyn wektora i macierzy: {C}')

    alfa=[1, 2, 3, 5, 7]
    n=4
    D=macierz_vandermonde(alfa, n)
    print(f'macierz Vandermonde: {D}')

    macierz_permutacji = [[0] *3 for i in range(3)]
    macierz_permutacji[0][0] = macierz_permutacji[1][0] = 0
    macierz_permutacji[2][0] = 1
    macierz_permutacji[1][1] = macierz_permutacji[2][1] = 0
    macierz_permutacji[0][1] = 1
    macierz_permutacji[0][2] = macierz_permutacji[2][2] = 0
    macierz_permutacji[1][2] = 1
    wynik=czy_macierz_permutacji(macierz_permutacji)
    print(macierz_permutacji)
    print(f'czy macierz permutacji: {wynik}')

    macierz_permutacji[0][0] = 1
    wynik=czy_macierz_permutacji(macierz_permutacji)
    print(macierz_permutacji)
    print(f'czy macierz permutacji: {wynik}')

if __name__ == '__main__':
    main()
