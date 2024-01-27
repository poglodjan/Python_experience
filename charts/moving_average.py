import random
import math
import numpy as np
import matplotlib.pyplot as plt

def moving_average(x, k, n):
    t=[0]*200
    suma,i,mian=0,0,0
    for l in range(n):
        i=l
        while i<n-l-1:
            suma+=x[i-l]
            i+=1
            mian+=0
    return t

def main():
    #random.seed(123)
    n = 100
    s = 1 
    k = 2*random.randint(1,50)+1
    x = np.cumsum([random.normalvariate(0, s) for i in range(n)])   
    plt.plot(x, color="black")
# tutaj narysuj wygładzoną wersję x, wywołując moving_average i plt.plot...
    t = moving_average(x,k,n)
    print(t)
    plt.plot(t, color="blue")
# użyj różnych kolorów dla różnych wartości parametru k
    plt.show()
if __name__ == '__main__':
   main()