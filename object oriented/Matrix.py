class Matrix():
    __slots__=['__data', '__shape']

    @staticmethod
    def isnumber(x):
        return type(x)==int or type(x)==float

    def __init__(self,nrow,ncol,data=0.0):
        if type(nrow) != int or type(ncol) != int:
            raise TypeError("Wrong parameter type")
        if nrow <= 0 or ncol <= 0:
            raise ValueError("Wrong parameter value")

        self.__shape=[nrow,ncol]
        self.__data=[None]*nrow*ncol
        if Matrix.isnumber(data):
            for i in range(self.__shape[0]*self.__shape[1]):
                self.__data[i]=data
        elif type(data) == list:        
            for i in range(nrow):
                for j in range(ncol):
                    self.__data[i*ncol+j] = data[i][j] #tworzyy __data
        else:
            raise TypeError("Wrong parameter type")

    def __repr__(self):
        return f"Matrix(__shape={self.__shape}, __data={self.__data})"
    def __str__(self):
        res = f"Matrix with {self.__shape[0]} rows and {self.__shape[1]} columns:\n"
        for i in range(self.__shape[0]):
            for j in range(self.__shape[1]):
                res += f"{self.__data[i * self.__shape[1] + j]: 6.2f}"
            res += "\n"
        return res
    
    def nrow(self):
        #Zwraca liczbe wierszy
        return self.__shape[0]

    def ncol(self):
        #Zwraca liczbe kolumn
        return self.__shape[1]

    def __add__(self, other):
        """
        Przeciazamy metode __add__
        Matrix + Matrix
        Matrix + cos
        """
        res = Matrix(self.__shape[0], self.__shape[1])
        if Matrix.isnumber(other):
            for i in range(res.__shape[0] * res.__shape[1]):
                res.__data[i] = self.__data[i] + other
            return res
        elif type(other) == Matrix:
            if self.__shape[0] != other.__shape[0] or self.__shape[1] != other.__shape[1]:
                raise ValueError("Wrong parameter value")
            for i in range(res.__shape[0] * res.__shape[1]):
                res.__data[i] = self.__data[i] + other.__data[i]
            return res
        else:
            raise TypeError("Wrong parameter type")
        
    def __radd__(self,other):
        #coś+Matrix
        return self + other

    def __mul__(self,other):
        #Matrix*Matrix, Matrix*coś
        ret =  Matrix(self.__shape[0], self.__shape[1], 0)
        if Matrix.isnumber(other): #mnozenie przez liczbe
            for i in range(self.__shape[0] * self.__shape[1]):
                ret.__data[i] = self.__data[i] * other
        elif type(other) == Matrix: #mnozenie przez macierz
            if self.__shape != other.__shape:
                raise ValueError("Wrong parameter value")
            for i in range(self.__shape[0] * self.__shape[1]):
                    ret.__data[i] = self.__data[i] * other.__data[i]
        else:
            raise TypeError("Wrong parameter type")
        return ret
    
    def __rmul__(self, other):
        return self * other
    
    def check_id(self, id):
        #Metoda pomocnicza, sprawdza poprawnosc indeksow"""
        if type(id) != tuple:
            return False
        if len(id) != 2:
            return False
        if type(id[0]) != int or type(id[1]) != int:
            return False
        if id[0] < 0 or id[0] >= self.__shape[0]:
            return False
        if id[1] < 0 or id[1] >= self.__shape[1]:
            return False
        return True

    def __getitem__(self, item):
        #Przeciazamy metode __getitem__ (indeksowanie), zwraca element w wierszu item[0] i kolumnie item[1]
        if not self.check_id(item):
            return None
        return self.__data[item[0] * self.__shape[1] + item[1]]

    def __setitem__(self, key, value):
        #Przeciazamy metode __setitem__ (indeksowanie), ustawia element w wierszu key[0] i kolumnie key[1] na wartosc value"""
        if self.check_id(key) and Matrix.isnumber(value):
            self.__data[key[0] * self.__shape[1] + key[1]] = value

def main():
    M1 = Matrix(3, 3, [[1, 2, 3],[4, 5, 6],[7, 8, 9]])
    M2 = Matrix(3, 3, 4.5)
    print(M1.__repr__())
    print(M2.__repr__())
    print(M1.__str__())
    print(M2.__str__())
    print(M1 + M2)
    print(M1 + 5)
    print(5 + M1)
    print(M1[1, 2])
    M1[1, 2] = 100.0
    print(M1)
    print(f"Liczba wierszy macierzy M1: {M1.nrow()}")
    print(f"Liczba kolumn macierzy M1: {M1.ncol()}")

if __name__ == "__main__":
    main()