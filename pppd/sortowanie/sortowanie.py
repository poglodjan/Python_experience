import random

def sortowanie_babelkowe(lista):
    n = len(lista)
    porownan=0
    zamiany=0
    while n > 1:
        zamien = False
        for l in range(0, n-1):
            porownan+=1
            if lista[l] > lista[l+1]:
                zamiany+=1
                lista[l], lista[l+1] = lista[l+1], lista[l]
                zamien = True
        n -= 1
        if zamien == False: break
    return lista, porownan, zamiany

def przez_wstawianie(lista):
    porownan=0
    zamiany=0
    n=len(lista)
    for i in range(1,n):
        klucz = lista[i]
        porownan+=1
        j = i - 1
        while j>=0 and lista[j]>klucz:
            lista[j + 1] = lista[j]
            zamiany+=1
            j = j - 1
        lista[j + 1] = klucz
        zamiany+=1
    return lista, porownan, zamiany

def sortuj_wybor(tab):
    n=len(tab)
    zamiany=0
    porownan=0
    for x in range(n-1): 
        minimum = x 
        for j in range(x+1, n):  
            porownan+=1
            if tab[j] < tab[minimum]:
                minimum = j 
                zamiany+=1    
        if x != minimum:
            pom = tab[x] 
            tab[x] = tab[minimum]
            zamiany+=1
            tab[minimum] = pom
    return tab, porownan, zamiany

def main():
    n=int(input('podaj n:'))
    pylo=[0]*(n+1)
    for i in range(n):
        pylo[i]=random.randint(0,100)

    b_pylo,b_porownan,b_zamiany=sortowanie_babelkowe(pylo)
    print(f'sortowanie bąbelkowe, porównań: {b_porownan} zamian: {b_zamiany}')

    w_pylo,w_porownan, w_zamiany=przez_wstawianie(pylo)
    print(f'przez wstawianie, porównań: {w_porownan} zamian: {w_zamiany}')

    wyb_pylo,wyb_porownan, wyb_zamiany=sortuj_wybor(pylo)
    print(f'przez wybór, porównań: {wyb_porownan} zamian:{wyb_zamiany}')

if __name__ == '__main__':
   main()