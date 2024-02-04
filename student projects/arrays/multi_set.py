def podaj():
    print('Podaj rozmiar zbioru:')
    max_el=int(input())
    lista=[0]*(max_el)
    for i in range(max_el):
        lista[i]=int(input(f'Podaj ilość {i}:'))
    if lista[max_el-1]==0:
        raise Exception('Lista nie spełnia warunków zadania')
    return lista

def wypisz(lista):
    wielkosc=0
    for i in range(len(lista)):
        wielkosc+=lista[i]
    poczatek,koniec,gasienica=0,0,0
    pylo=[0]*wielkosc
    for i in range(len(lista)):
        n=lista[i]
        if n==0:
            continue
        else:
            while n>0:
                pylo[gasienica]+=i
                gasienica+=1
                n-=1
    return pylo
        
def dodaj(zbior, element):
    n=len(zbior)
    zbior = zbior+[0]
    zbior[n] = element
    for i in range(n-1):
        if zbior[i]==element: czy_byl_wczesniej=True
        else: czy_byl_wczesniej=False
    return zbior, czy_byl_wczesniej

def roznica(zbiorA,zbiorB):
    return 0

def przeciecie(zbiorA, zbiorB):
    n=len(zbiorA)
    m=len(zbiorB)
    gasienica=0
    if n<m: 
        min=n
    else: 
        min=m
    pylo=[]
    for i in range(min):
        if zbiorA[i]==0 or zbiorB[i]==0:
            continue
        elif zbiorA[i]==zbiorB[i]:
            n=zbiorB[i]
            while n>0:
                pylo=pylo+[0]
                pylo[gasienica]+=i
                gasienica+=1
                n-=1
        elif zbiorA[i]>zbiorB[i]:
            n=zbiorB[i]
            while n>0:
                pylo=pylo+[0]
                pylo[gasienica]+=i
                n-=1
                gasienica+=1
        elif zbiorA[i]<zbiorB[i]:
            n=zbiorA[i]
            while n>0:
                pylo=pylo+[0]
                pylo[gasienica]+=i
                n-=1
                gasienica+=1
    return pylo

def r(zbiorA, zbiorB):
    n=len(zbiorA)
    m=len(zbiorB)
    gasienica=0
    if n<m: 
        min,max=n,m
    else: 
        min,max=m,n
    pylo=[]
    for i in range(min):
        if zbiorA[i]==0 or zbiorB[i]==0:
            continue
        elif zbiorA[i]==zbiorB[i]:
            continue
        elif zbiorA[i]>zbiorB[i]:
            pylo=pylo+[0]
            w=zbiorA[i]-zbiorB[i]
            while w>0:
                pylo[gasienica]+=i
                w-=1
        elif zbiorA[i]<zbiorB[i]:
            w=zbiorB[i]-zbiorA[i]
            while w>0:
                pylo=pylo+[0]
                pylo[gasienica]+=i
                gasienica+=1
                w-=1
    return pylo

def main():
    multiA=podaj()
    print(f'Podany zbiór to: \n {wypisz(multiA)}')
    listaA=wypisz(multiA)
    element=int(input(f'Podaj nowy element ze zbioru A:\n'))

    listaA,sprawdzenie=dodaj(listaA, element)
    print(f'Zbiór A po dodaniu elementu:\n {listaA}')

    if sprawdzenie==True:
        multiA[len(multiA)-1]+=1
    if sprawdzenie==False:
        if element==(len(multiA)):
            multiA+=[0]
            multiA[len(multiA)-1]+=1
        else:
            roznica=(element-len(multiA))
            nowa_lista=[0]*roznica
            multiA+=nowa_lista
            multiA[len(multiA)-1]+=1

    multiB=podaj()
    print('Przecięcie zbiorów:')

    przec=przeciecie(multiA,multiB)
    print(f'Przecięcie zbiorów:\n {przec}')

    roznica=r(multiA,multiB)
    print(f'Róznica zbiorów:\n {roznica}')
    
    
if __name__ == '__main__':
   main()
