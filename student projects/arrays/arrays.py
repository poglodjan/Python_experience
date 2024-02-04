PRZYKLADOWE_DANE = [(1, 10),  (12, 30), (15, 25), (26, 29), (7, 21),  (32, 38)]
N = 40

def wypisz_os(x_max, krok):
    print('0', end='')
    i = krok
    while i <= x_max:
        print(f'{i:.>{krok}d}', end='')
        i += krok
    print('.' * (x_max - i))

def wypisz_przedzialy(przedzialy, x_max=N, krok=5):
    assert isinstance(przedzialy, list), "Podany obiekt nie jest listą."
    wypisz_os(x_max, krok)
    for i in range(len(przedzialy)):
        if not (isinstance(przedzialy[i], tuple) or isinstance(przedzialy[i], list)):
            print(f'Przedział {i} nie jest listą/krotką.')
        elif len(przedzialy[i]) != 2:
            print(f'Przedział {i} nie ma długości 2.')
        elif not (0 <= przedzialy[i][0] < przedzialy[i][1] <= x_max):
            print(f'Nieprawidłowe końce przedziału: "{przedzialy[i]}"')
        else:
            a, b = przedzialy[i]
            print(' ' * a + '#' * (b - a + 1) + ' ' * (x_max - b), end='')
            print(f' [{a:2d}, {b:2d}], dlugosc={b - a + 1}')


def odleglosc(prz1, prz2):
    a = max(prz1[0], prz2[0])
    b = min(prz1[1], prz2[1])
    if b < a:
        return a - b
    else:
        return 0


def znajdz_bliskie(przedzialy, k):
    wynik = []
    for i in range(len(przedzialy)):
        for j in range(i):
            d = odleglosc(przedzialy[i], przedzialy[j])
            if 0 < d <= k:
                wynik.append([przedzialy[j], przedzialy[i], d])
    return wynik


def skurcz(przedzialy, k, d):
    assert isinstance(k, int) and k >= 1
    wynik = []
    for i in range(len(przedzialy)):
        a, b = przedzialy[i]
        a += k
        b -= k
        if b - a + 1 >= d:
            wynik.append((a, b))
    return wynik


def main():
    dane = PRZYKLADOWE_DANE

    k = 2
    d = 3
    print(f'### Kurczenie (k = {k}, d = {d}):')
    print('Oryginalne dane:')
    wypisz_przedzialy(dane)
    print('Skurczone:')
    wypisz_przedzialy(skurcz(dane, k, d))

    print(f"""### Odległość:
    odleglosc((5, 10), (13, 15)) == 3:    
    {odleglosc((5, 10), (13, 15)) == 3}
    odleglosc((5, 10), (11, 15)) == 1:
    {odleglosc((5, 10), (11, 15)) == 1}
    odleglosc((5, 10), (10, 15)) == 0:
    {odleglosc((5, 10), (10, 15)) == 0}
    odleglosc((5, 10), (7,  15)) == 0:
    {odleglosc((5, 10), (7, 15)) == 0}
    """)

    print('### Bliskie przedziały (k = 3):')
    print('Przedziały:')
    bliskie = znajdz_bliskie(dane, 3)
    print(bliskie)
    print('Wykresy:')
    wypisz_przedzialy(dane)
    for i in range(len(bliskie)):
        wypisz_przedzialy([bliskie[i][0], bliskie[i][1]])
    print()

    # wypisz_przedzialy([(10, 20), (30, 35)])


if __name__ == '__main__':
    main()
