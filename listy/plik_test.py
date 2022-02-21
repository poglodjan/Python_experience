def zapis(napis1, napis2, napis3, pliczek): 
    with open(pliczek , 'w') as zapisz: 
        zapisz.write(f'{napis1} \n {napis2} \n {napis3} \n') #zapisujemy w pliczku słowa

def odczyt(pliczek):
    with open(pliczek, 'r') as odczyt: 
        odczyt1 = odczyt.readline() #odczytujemy 1 linijke
        odczyt2 = odczyt.readline() #odczytujemy 2 linijkę
        odczyt3 = odczyt.readline() #odczytujemy 3 linijkę
    
    return odczyt1, odczyt2, odczyt3 #zwracamy odczytane słowa

def main():

    napis1 = 'ala'
    napis2 = 'ma'
    napis3 = 'kota'
    pliczek = 'file.txt'

    zapis(napis1, napis2, napis3, pliczek) #przenosimy słowa ala ma kota do funkcji zapis

    odczyt1, odczyt2, odczyt3 = odczyt(pliczek) #przenosimy odczytane słowa z funkcji odczyt do main

    print(f'{odczyt1} {odczyt2} {odczyt3}') #wypisujemy odczytane słowa

if __name__ == '__main__':
    main()