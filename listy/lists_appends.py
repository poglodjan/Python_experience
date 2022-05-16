def split_codes(x, f):
    k = max(f) + 1
    lista_pomoc = [[] for _ in range(k)]
    for i in range(k):
        for j in range(len(f)):
            if f[j] == i:
                lista_pomoc[i].append(x[j])
    return lista_pomoc

def split_codes(x, f):
    k = max(f) + 1
    lista_pomoc = [[] for _ in range(k)]
    for j in range(len(f)):
        lista_pomoc[f[j]].append(x[j])
    return lista_pomoc
