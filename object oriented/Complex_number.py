import math

class Zespolona:
    __slots__=['re','im']
    def __init__(self, re, im):
        self.re=re
        self.im=im
    def __repr__(self):
        return f'Zespolona(re={self.re}, im={self.im})'
    def __str__(self):
        return f'{self.re}+{self.im}i'

    def __add__(self, other):
        if type(other)!=Zespolona:
            return None
        wynik_czesc_rzeczywista=self.re+other.re
        wynik_czesc_urojona=self.im+other.im
        wynik=Zespolona(wynik_czesc_rzeczywista,wynik_czesc_urojona)
        return wynik

    @staticmethod
    def tworz_kata(kat,promien):
        rzeczywista = promien * math.cos(kat)
        urojona = promien * math.sin(kat)
        wynik = Zespolona(rzeczywista,urojona)
        return wynik

    def modul(self):
        wynik=self.re**2+self.im**2
        return math.sqrt(wynik)
    
    def powiel(self, x):
        self.re*=x
        self.im*=x
    
    def __eq__(self, other):
        return abs(self.re - other.re) < 1e-7 and abs(self.im - other.im) < 1e-7

    def __ne__(self,other):
        return not self==other
    
def main():
    z1=Zespolona(1,2)
    z2=Zespolona(3,4)

    print(z1) #Korzysta z str
    print([z1,z2]) #jak robimy elementy z listy to korzystamy z repr

    print(z1+z2) #__add__
    print(z1+0)

    z3 = Zespolona.tworz_kata(math.pi / 4, 5) #statystyczna
    print(z3)

    print(z1.modul())

    z1.powiel(5)
    print(z1)

    z4 = Zespolona(0.1 + 0.1 + 0.1, 0.3 + 0.3 + 0.3)
    z5 = Zespolona(0.3, 0.9)

    print(z4==z5)
    print(z4==Zespolona(1,2))

    print(z4!=z5)
    print(z4!=Zespolona(1,2))
    
if __name__ == "__main__":
    main()