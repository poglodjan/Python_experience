import random
import matplotlib.pyplot as plt

def sito_eratostenesa(n):
    lista=[0]
    pylo=[False]*(n + 1)
    i = 2
    while i * i <= n:
        if  not pylo[i]:
            j = i * i            
            while j <= n:
                pylo[j] = True
                j += i
        i += 1
    for i in range(2, n+1):
        if not pylo[i]:
            lista.append(i)
    return pylo

def main(): 
    n=int(input('wprowadz n:'))
    k=int(input('wprowadz liczbe kolumn:'))
    rysuj=' '
    pylo = sito_eratostenesa(n)
    for i in range(1,n):
        if pylo[i]==0:
            rysuj+='o'
        if pylo[i]==1:
            rysuj+='.'
        if i%k==0:
            rysuj+='\n'
    print(rysuj)

    x=[i for i in range(0,n+1)]
    print(x)
    
    plt.scatter(x, pylo)
    plt.show()

if __name__ == '__main__':
   main()
