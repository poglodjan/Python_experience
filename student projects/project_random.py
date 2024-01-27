import random

def mozliwe_akcje():
    print("1 - atak")
    print("2 - ucieczka")
    print("3 - kung-fu")
    print("4 - zapisz gre")
    print("5 - odczytaj gre")

def wypisz_zycie(zycie):
    print(f'Masz jeszcze {zycie} punktów zycia')

def pobierz_akcje():
    x = int(input())
    while x>5 or x<1:
        print('wybierz akcje jeszcze raz!')
        x=int(input())
    return x

def zapisz_gre(zycie, ile_dokungfu, gdzie):

    with open(gdzie, 'w') as plik:
        plik.write(f'{zycie} \n {ile_dokungfu}')

def wczytaj_gre(gdzie):
    with open(gdzie, 'r') as odczyt:
        zycie=int(odczyt.readline())
        ile_dokungfu = int(odczyt.readline())
    return zycie, ile_dokungfu

def main():
    zycie = 500
    ile_dokungfu = 0

    while zycie > 0:
        print("\n")
        sila_goblina=random.randint(0,200)
        ilosc_zlota=random.randint(0,200)
        print(f'Straznik o sile {sila_goblina} broni {ilosc_zlota} sztuk zlota')
        wypisz_zycie(zycie)

        mozliwe_akcje()
        krok = pobierz_akcje()
        
        if krok == 4:
            plik = str(input("Podaj sciezke do pliku, w ktorym ma byc zapisana gra: "))
            zapisz_gre(zycie, ile_dokungfu)

        if krok == 5:

            plik = str(input("Podaj sciezke do pliku, w ktorym jest zapisana gra: "))
            zycie, ile_dokungfu = wczytaj_gre(plik)
         

if __name__ == '__main__':
    main()
