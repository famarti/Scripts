#burbujeo.py


def esta_ordenada(lista):
    return all(a <= b for a, b in zip(lista, lista[1:]))

def ord_burbujeo(lista):
    reco = 0  # nro recorridas
    comp = 0  # nro comparaciones
    while esta_ordenada(lista) == False:
        reco += 1
        for i in range(len(lista) - 1):
            if lista[i+1] < lista[i]:
                lista[i+1], lista[i] = lista[i], lista[i+1]
                comp += 1
            else:
                comp += 1
            print("DEBUG: ", lista)
    return comp, reco

def ord_burbuejo_rec(lista):
    if esta_ordenada(lista):
        return lista
    for i in range(len(lista)-1):
        if lista[i+1] < lista[i]:
            lista[i+1], lista[i] = lista[i], lista[i+1]
    return ord_burbuejo_rec(lista)