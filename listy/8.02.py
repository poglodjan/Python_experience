import csv
import numpy
import matplotlib.pyplot as plt

def transpozycja(iris):
    n=len(iris)
    m=len(iris[0])
    y=[ [0]*n for i in range(m)]
    for w in range(m):
        for k in range(n):
            y[w][k]=iris[k][w]
    return y

def main():
    iris = []
    f = open("iris.csv", "r")  
    for row in csv.reader(f):
        for i in range(len(row)):
            row[i] = float(row[i])  
            list.append(iris, row)  
    f.close()

    y=transpozycja(iris)

    zmienna_x=[0]*len(y[0])
    zmienna_y=[0]*len(y[0])

    for i in range(0, len(y[0])):
        for i in range(0, len(y[0])):
            zmienna_x[i]=y[1][i]
            zmienna_y[i]=y[2][i]

    print(len(y[0]))
    plt.figure(figsize=[8, 8], dpi=72)
    plt.scatter(zmienna_x, zmienna_y)

    plt.show()

if __name__ == '__main__':
    main()

