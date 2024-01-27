import random

def read_data(datafile):
    extracted_data = [i.strip().split() for i in open(datafile)]
    flat_list = [int(item) for sublist in extracted_data for item in sublist]
    return flat_list


def validate(n, d, dlugosc_listy):
    if not type(n) == int:
        print('Wrong data, try again')
        main()
    if not type(d) == int:
        print('Wrong data, try again')
        main()
    if n < d:
        print('Wrong data, try again')
        main()
    if dlugosc_listy>(n-1):
        print('Wrong data, try again')
        main()


def merge_islands(lista,n, d):
    dl=len(lista)
    for i in range(0,dl,2):
        poczatek=i
        koniec=i+1
        for j in range(koniec+1,dl,2):
            if j>koniec:
                lista[koniec]=lista[j+1]
                if j<dl-2:
                    klucz1=lista[j]
                    klucz2=lista[j+1]
                    lista.remove(klucz1)
                    lista.remove(klucz2)
            poczatek+=2
            koniec+=2
    return lista

def create_map(lista, n, d):
    mapa=['_']*n
    dl=len(lista)
    for i in range(0,dl,2):
        pocz=lista[i]
        koniec=lista[i+1]
        roznica=koniec-pocz
        for k in range(0,roznica):
            mapa[k]='|'
    for i in range(dl):
        if mapa[i]=='|':
            for l in range(1,d):
                mapa[i-d]='-'
                mapa[i+d]='-'
    return mapa


def main():
    d = int(input('provide length of island:'))  # odległość
    n = int(input('provide map length:'))  # długość mapy
    plik = input('Upload file:')  # plik

    lista = read_data(plik)  # 'koordynaty_wysp_zadA.csv'
    lista=[3,5,4,7,10,15]
    length=len(lista)  
    validate(n, d, length)
    nowa_lista=merge_islands(lista,n,d)
    mapa=create_map(nowa_lista,n,d)
    print(nowa_lista)

if __name__ == '__main__':
    main()
