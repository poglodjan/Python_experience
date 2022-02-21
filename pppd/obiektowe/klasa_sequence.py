import math

class Sequence:
    def __init__(self, n, wyr):

        if not (type(n) is int and n > 0):
            raise Exception("Zła długość ciągu")

        if type(wyr) == int:
            wart = [wyr for i in range(n)]
        elif len(wyr) == n and type(wyr[0]) == int and type(wyr) == list:
            wart = wyr
        else:
            raise Exception("Złe wyrazy ciągu")
        self.__n = n
        self.__elements = [0 for i in range(n)]
        for i in range(n):
            self.__elements[i] = wart[i]


    def Length(self):
        return self.__n

    def __repr__(self):
        wynik = f"Sequence with {self.__n} elements:"
        for i in range(self.__n):
            wynik += f"\n [{i}]:\t{self.__elements[i]}"
        return wynik

    def __mul__(self, other):
        if type(other) is not int:
            raise Exception("Mnożenie przez zły typ")
        wynik = Sequence(self.Length(), 0)
        for i in range(self.Length()):
            wynik.__elements[i] = self.__elements[i] * other
        return wynik

    def __matmul__(self, other):
        if not (type(other) is int or type(other) is float):
            raise Exception("Zły typ argumentu")
        if type(other) is int:
            dlugosc = self.Length() * other
        elif type(other) is float:
            dlugosc = math.floor(self.Length() * other)

        wartosci = [0 for i in range(dlugosc)]
        for i in range(dlugosc):
            wartosci[i] = self.__elements[i % self.Length()]

        return Sequence(dlugosc, wartosci)

    def Subsequence(self, x, y):
        if not (type(x) == int and type(y) == int and x < y):
            raise Exception("Dla takich danych podciąg nie jest zdefiniowany")

        dlugosc = y - x
        wartosci = [0 for i in range(dlugosc)]
        for i in range(dlugosc):
            wartosci[i] = self.__elements[x + i]

        return Sequence(dlugosc, wartosci)

    def Increasing(self):
        for i in range(self.Length() - 1):
            if not self.__elements[i] <= self.__elements[i+1]:
                return False
        return True

    def Decreasing(self):
        for i in range(self.Length() - 1):
            if not self.__elements[i] >= self.__elements[i + 1]:
                return False
        return True

    def Bitonic(self):
        for i in range(1, self.Length() - 1):
            S1 = self.Subsequence(0, i)
            S2 = self.Subsequence(i, self.Length())
            if (S1.Increasing and S2.Decreasing):
                return True
        if self.Increasing() or self.Decreasing():       #Sprawdzamy w ten sposób dla i = 0 i i = n-1
            return True
        return False

    def Sprawdz(self): #Sprawdza monotoniczność i bitoniczność ciągu, wypisuje wyniki
        wynik = self.__repr__()
        wynik += f"\nRosnacy:\t{self.Increasing()}\nMalejacy:\t{self.Decreasing()}\nBitoniczny:\t{self.Bitonic()}"
        print(wynik)

def main():

    S1 = Sequence(10, 1)
    S2 = Sequence(3, [1, 5, 8])
    print(f"Dlugosc S1 = {S1.Length()}")
    print(f"Dlugosc S2 = {S2.Length()}")
    print(S1)
    print(S2)
    S3 = S2 * 3
    S4 = S2 @ 2.5
    S5 = S2 @ 2.7
    print(S3)
    print(S4)
    print(S5)
    Podciag1 = S4.Subsequence(0, 7)
    Podciag2 = S4.Subsequence(0, 1)
    print(Podciag1)
    print(Podciag2)

    Spr1 = Sequence(6, [1, 2, 3, 4, 2, 1])
    Spr2 = Sequence(6, [1, 2, 3, 4, 7, 1])
    Spr3 = Sequence(6, [1, 2, 1, 0, -7, -8])
    Spr4 = Sequence(6, [1, 2, 3, 4, 5, 10])
    Spr5 = Sequence(6, [9, 8, 7, 6, 4, 1])

    Spr1.Sprawdz()
    Spr2.Sprawdz()
    Spr3.Sprawdz()
    Spr4.Sprawdz()
    Spr5.Sprawdz()


if __name__ == "__main__":
    main()
