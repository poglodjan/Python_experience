import numpy
import random
import math
import copy
from PIL import Image

def png_read(filepath):
    img = Image.open(filepath)
    assert len(img.size)==2 # skala szarosci, nie RGB
    return (numpy.array(img)/255).reshape(img.size[1], img.size[0]).tolist()

def png_write(img, filepath):
    img = Image.fromarray((numpy.array(img)*255).astype(numpy.int8), 'L')
    img.save(filepath)

def range_matrix(A):
    n=len(A)
    m=len(A[0])
    ret = [A[0][0], A[0][0]]
    for w in range(n):
        for k in range(m):

            kand=A[w][k]
            if ret[0]>kand:
                ret[0]=kand
            if ret[1]<kand:
                ret[1]=kand
    return ret

def czy_matrix(A):
    n=len(A)
    m=len(A[0])
    for w in range(n):
        if len(A[w])!=m:
            return False
    return True

def diagonala(A):
    for w in range(len(A)):
        for k in range(len(A[0])):
            if w!=k:
                A[w][k]=0.5
    return A


def rozjasnienie(A,b):
    n=len(A)
    m=len(A[0])
    y=copy.deepcopy(A)
    for w in range(n):
        for k in range(m):
            y[w][k]+=b
            if y[w][k]>1:
                y[w][k]=1
            if y[w][k]<0:
                y[w][k]=0
    return y

def negatyw(A):
    n=len(A)
    m=len(A[0])
    wynik=copy.deepcopy(A)
    for w in range(n):
        for k in range(m):
            wynik[w][k]=1-wynik[w][k]
    return wynik


def kontrast(A, theta):
    #funkcja f:
    def f(c, theta):
        x=1+math.exp(-theta*(c-0.5))
        return 1/x
    
    n=len(A)
    m=len(A[0])
    wynik=[ [0]*m for i in range(n) ]

    for w in range(n):
        for k in range(m):
            wynik[w][k]=f(A[w][k],theta)
    return wynik

def convolution(A, B):
    n=len(A)
    m=len(A[0])
    C= [ [0]*m for i in range(n) ]
    k=len(B)//2
    for i in range(n):
        for j in range(m):
            for u in range(-k,k+1):
                for v in range(-k, k+1):
                    if (i+u<n and i+u>=0) and (j+v<m and j+v>=0):
                        C[i][j]= A[i+u][j+v] * B[k+u][k+v]              
    return C

def main():
    A = png_read('astronom.png')
    if not czy_matrix(A):
        raise ValueError("nie macierz")
    print('** 1-rozjasnienie **\n'
    '** 2-negatyw **\n'
    '** 3-min i max **\n'
    '** 4-kontrast **\n'
    '** 5-convolution')

    wyb=int(input())
    min_max=range_matrix(A)
    if wyb==1:
        b=float(input())
        y=rozjasnienie(A,b)
    if wyb==2:
        y=negatyw(A)
    if wyb==3:
        print(min_max)
    if wyb==4:
        theta=float(input())
        y=kontrast(A,theta)
    if wyb==5:
        k=int(input('podaj k:'))
        l=(2*k+1)
        B=[ [1/(l**2)]*l  for i in range(l) ]
        print(B)
        y=convolution(A,B)
    if wyb==6:
        y=diagonala(A)
    
    png_write(y, "output.png")

if __name__ == '__main__':
   main()
