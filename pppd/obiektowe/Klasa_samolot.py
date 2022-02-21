import copy

class Samolot():
    __slots__=['__nazwa','__wiersze','__kolumny', '__miejscei','__wykonanie_rezerw']

    def __init__(self, nazwa, liczba_rzedow, liczba_miejsc_w_rzedzie):
        self.__wykonanie_rezerw=0
        self.__miejscei=[0]*liczba_miejsc_w_rzedzie*liczba_rzedow
        self.__nazwa=nazwa
        self.__wiersze=liczba_rzedow
        self.__kolumny=liczba_miejsc_w_rzedzie
        if type(self.__wiersze)!=int or type(self.__kolumny)!=int or type(self.__nazwa)!=str:
            raise ValueError('niepoprawne dane')
    def __repr__(self):
        krok=1
        wypis=f'{self.__nazwa}\n  A B C D \n'
        for i in range(self.__wiersze):
            wypis+=f'{krok}'
            for j in range(self.__kolumny):
                pom=i*self.__kolumny+j
                wypis+=f' {self.__miejscei[pom]}'
            wypis+='\n'
            krok+=1
        return wypis

    def rezerwuj_miejsce(self,numer_miejsca):   
        rzad=numer_miejsca[0]
        kolumna=numer_miejsca[1]
        if kolumna=='A': kolumna=1
        if kolumna=='B': kolumna=2
        if kolumna=='C': kolumna=3
        if kolumna=='D': kolumna=4
        i=(4*(int(rzad)-1)+int(kolumna))-1
        if self.__miejscei[i]==0:
            self.__miejscei[i]=1
            self.__wykonanie_rezerw+=1
            return True
        else: return False

    def sprawdz_czy_miejsce_wolne(self, numer_miejsca):
        rzad=numer_miejsca[0]
        kolumna=numer_miejsca[1]
        if kolumna=='A': kolumna=1
        if kolumna=='B': kolumna=2
        if kolumna=='C': kolumna=3
        if kolumna=='D': kolumna=4
        i=(4*(int(rzad)-1)+int(kolumna))-1
        if self.__miejscei[i]==0:
            return True
        else: return False

    def ile_wolnych_miejsc(self):
        wynik=(self.__wiersze*self.__kolumny)-self.__wykonanie_rezerw
        return wynik+1
    
    @staticmethod
    def skopiuj_samolot_z_rezerwacjami(samolot, nowa_nazwa):
        kopia = Samolot(nowa_nazwa, samolot.__wiersze, samolot.__kolumny)

        for i in range(len(samolot.__miejscei)):
                kopia.__miejscei[i] = samolot.__miejscei[i]
                kopia.__wykonanie_rezerw = samolot.__wykonanie_rezerw

        return kopia
    
    def __sub__(self, other):
        if self.__kolumny!=other.__kolumny or self.__wiersze!=other.__wiersze:
            raise Exception('miejsca w samolotach są rózne!')
        samolot_roznica=Samolot('Roznica', self.__wiersze, self.__kolumny)
        for i in range(len(self.__miejscei)):
            if self.__miejscei[i]!=other.__miejscei[i]:
                samolot_roznica.__miejscei[i]=1
        return samolot_roznica
        

def main():
    nr_etapu=1
    print(f'------------Etap {nr_etapu}-----------------------')
    nr_etapu+=1
    airbus = Samolot('Embraer 190', 5, 4)
    print(airbus)
    print(f'------------Etap {nr_etapu}-----------------------')
    nr_etapu+=1
    numer='3B'
    print(f'czy miejsce {numer} jest wolne?: {airbus.sprawdz_czy_miejsce_wolne(numer)}')
    airbus.rezerwuj_miejsce('3B')
    print(airbus)
    print(f"Rezerwacja miejsca 1A zakończkona: {airbus.rezerwuj_miejsce('1A')}")
    print(f"Rezerwacja miejsca 2b zakończkona: {airbus.rezerwuj_miejsce('2B')}")
    print(f"Rezerwacja miejsca 3C zakończkona: {airbus.rezerwuj_miejsce('3C')}")
    print(f"Rezerwacja miejsca 4D zakończkona: {airbus.rezerwuj_miejsce('4D')}")
    print(f"Rezerwacja miejsca 5C zakończkona: {airbus.rezerwuj_miejsce('5C')}")
    print(f"Rezerwacja miejsca 4B zakończkona: {airbus.rezerwuj_miejsce('4B')}")
    print(f"Rezerwacja miejsca 3A zakończkona: {airbus.rezerwuj_miejsce('3A')}")
    print(f"Rezerwacja miejsca 3A zakończkona: {airbus.rezerwuj_miejsce('3A')}")
    assert not airbus.sprawdz_czy_miejsce_wolne('3A')
    assert airbus.sprawdz_czy_miejsce_wolne('4C')
    print()
    print(airbus)

    print(f'------------Etap {nr_etapu}-----------------------')
    nr_etapu+=1
    print(airbus.ile_wolnych_miejsc())

    print(f'------------Etap {nr_etapu}-----------------------')
    nr_etapu+=1
    airbus_kopia = Samolot.skopiuj_samolot_z_rezerwacjami(airbus, 'Embraer 190+')
    print(airbus_kopia)

    print(f"Rezerwacja miejsca 1B zakończkona: {airbus_kopia.rezerwuj_miejsce('1B')}")
    print(f"Rezerwacja miejsca 1C zakończkona: {airbus_kopia.rezerwuj_miejsce('1C')}")
    print(f"Rezerwacja miejsca 1D zakończkona: {airbus_kopia.rezerwuj_miejsce('1D')}")
    assert airbus.sprawdz_czy_miejsce_wolne('1B'), "Kopia się nie udała"
    assert airbus.sprawdz_czy_miejsce_wolne('1C'), "Kopia się nie udała"
    assert airbus.sprawdz_czy_miejsce_wolne('1D'), "Kopia się nie udała"
    print(airbus)
    print(airbus_kopia)

    print(f'------------Etap {nr_etapu}-----------------------')
    samolot_z_roznica = airbus_kopia - airbus
    print(samolot_z_roznica)


if __name__ == "__main__":
    main()