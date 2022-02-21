def horner(tablica, left, right, x):
    i = right
    result = tablica[i]
    while i > left:
        print(result)
        i = i - 1
        result = result * x + tablica[i]
    return result

poly = [1, 2, 3, 4]
y = 2
result = horner(poly, 0, len(poly)-1, y)
