import random
import math
import matplotlib.pyplot as plt

def odchylenia_s(tabx, taby, n, x_s, y_s):
    odchx = 0
    odchy = 0
    for i in range(n):
        odchx += (tabx[i]-x_s)**2
        odchy += (taby[i]-y_s)**2
    odchx = math.sqrt(odchx/(n-1))
    odchy = math.sqrt(odchy/(n-1))
    return odchx, odchy

def r(tabx, taby, n, x_s, y_s):
    suma, licznik = 0,0
    sx, sy = odchylenia_s(tabx, taby, n, x_s, y_s)
    for i in range(n):
        licznik+=(tabx[i]-x_s)*(taby[i]-y_s)
        suma+=licznik/(sx*sy)
    return suma/(n-1)    

def E(alfa, beta,tabx, taby, n):
   suma=0
   for i in range(n):
       suma += (alfa+beta*tabx[i]-taby[i])**2
   return suma

def regresja():
   n = int(input())
   tabx = []
   taby = []
   alfa, sumax, beta, sumay = 0,0,0,0
   for i in range (n):
       tabx.append(random.randint(-10,10))
       taby.append(random.randint(-10,10))
       sumax+=tabx[i]
       sumay+=taby[i]
   x_s=sumax//n
   y_s=sumay//n

   for i in range(n):
       s1 = (tabx[i] - x_s)*(taby[i] - y_s)
       s2 = (tabx[i]-x_s)**2
       if s2!=0:
           beta += s1/s2

   alfa = y_s - beta * x_s
   return beta, alfa, n, tabx, taby, x_s, y_s

def main():
   alfa, beta, n, tabx, taby, x_s, y_s = regresja()
   wsp_e = E(alfa, beta,tabx, taby, n)
   wsp_k_l = r(tabx, taby, n, x_s, y_s)

   print(f'prosta: y = {beta}*x + {alfa}')
   print(f'współczynnik E = {wsp_e}')
   print(f'współczynnik korelacji liniowej = {wsp_k_l}')

   random.seed(123)
   alpha0 = alfa
   beta0 = beta
   # poniżej używamy tzw. wyrażenia listotwórczego (ang. list comprehension)
   x = [tabx[i] for i in range(n)]
   y = [alpha0 + beta0 * x[i] + random.normalvariate(0, 1) for i in range(n)]
   # czyli y=alpha0+beta0*x+szum z rozkładu normalnego N(0,1)
   
   # wykres rozproszenia:
   plt.scatter(x, y)
   # rysowanie odcinka [xmin, xmax], [ymin, ymax]:
   plt.plot([-10, 10], [alpha0 + beta0 * (-10), alpha0 + beta0 * 10], color="red")
   plt.show()


if __name__ == '__main__':
   main()



