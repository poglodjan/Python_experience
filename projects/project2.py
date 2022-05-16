import random

def rzucaj(p, l_rzutów):
    rzuty=[random.randint(1,6) for k in range(l_rzutów)]
    return rzuty

def sprawdz(rzuty, n):
    dystans=0
    ile_do_dwoch=0
    czy_doszedl=False
    for i in range(len(rzuty)):
        oczka=rzuty[i]
        if oczka%2==0:
            dystans+=rzuty[i]
            ile_do_dwoch=0
        elif oczka%2!=0 and ile_do_dwoch<2:
            dystans-=rzuty[i]
            ile_do_dwoch+=1
        elif oczka%2!=0 and ile_do_dwoch==2:
            nowa_liczba=random.randint(1,6)
            rzuty[i]=nowa_liczba
            if nowa_liczba%2==0:
                dystans+=rzuty[i]
                ile_do_dwoch=0
            if nowa_liczba%2==0:
                dystans-=rzuty[i]
                ile_do_dwoch=0
    if dystans>=n:
        czy_doszedl=True
    return czy_doszedl, dystans

def main():
    random.seed(9876)
    p=int(input())
    n=int(input())
    ile_kroków=[0]*p
    czy_udalo=[0]*p
    kroki=0
    lista=[random.randint(5,20)*2 for i in range(p)]
    próba=1
    while p>0:
        print(f'próba numer {próba}')

        l_rzutow=lista[próba-1]
        rzuty = rzucaj(p, l_rzutow)
        
        czy_doszedl, kroki = sprawdz(rzuty, n)
        print(f'Rzuty: {rzuty}')
        print(f'Wykonując {len(rzuty)} rzutów udało się pokonać {kroki} kroków')
        if n<=kroki:
            n=0
            alfa=0
            czy_udalo[próba-1]=True
        else:
            czy_udalo[próba-1]=False
            alfa=n-kroki
        
        ile_kroków[próba-1]=kroki
        print(f'do pokonania zostało {alfa} kroków\n')
        próba+=1
        p-=1
    print(ile_kroków)    
    print(czy_udalo)

if __name__ == '__main__':
   main()
