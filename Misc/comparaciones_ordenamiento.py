# comparaciones_ordenamiento.py
import random
import numpy as np
import matplotlib.pyplot as plt
#%% seleccion
def ord_seleccion(lista):
    """Ordena una lista de elementos según el método de selección.
       Pre: los elementos de la lista deben ser comparables.
       Post: la lista está ordenada."""

    # posición final del segmento a tratar
    n = len(lista) - 1

    # mientras haya al menos 2 elementos para ordenar
    comp = 0
    while n > 0:
        # posición del mayor valor del segmento
        p = buscar_max(lista, 0, n)
        comp += (n - 0)
        # intercambiar el valor que está en p con el valor que
        # está en la última posición del segmento
        lista[p], lista[n] = lista[n], lista[p]
        #print("DEBUG: ", p, n, lista)

        # reducir el segmento en 1
        n = n - 1
    return comp
def buscar_max(lista, a, b):
    """Devuelve la posición del máximo elemento en un segmento de
       lista de elementos comparables.
       La lista no debe ser vacía.
       a y b son las posiciones inicial y final del segmento"""

    pos_max = a
    for i in range(a + 1, b + 1):
        if lista[i] > lista[pos_max]:
            pos_max = i
    return pos_max
#%% insercion
def ord_insercion(lista):
    """Ordena una lista de elementos según el método de inserción.
       Pre: los elementos de la lista deben ser comparables.
       Post: la lista está ordenada."""
    comp = 0
    for i in range(len(lista) - 1):
        # Si el elemento de la posición i+1 está desordenado respecto
        # al de la posición i, reubicarlo dentro del segmento [0:i]
        if lista[i + 1] < lista[i]:
            comp += reubicar(lista, i + 1)
        else:
            comp += 1
        #print("DEBUG: ", lista)
    return comp
def reubicar(lista, p):
    """Reubica al elemento que está en la posición p de la lista
       dentro del segmento [0:p-1].
       Pre: p tiene que ser una posicion válida de lista."""
    v = lista[p]
    comps = 0
    # Recorrer el segmento [0:p-1] de derecha a izquierda hasta
    # encontrar la posición j tal que lista[j-1] <= v < lista[j].
    j = p
    while j > 0 and v < lista[j - 1]:
        # Desplazar los elementos hacia la derecha, dejando lugar
        # para insertar el elemento v donde corresponda.
        lista[j] = lista[j - 1]
        j -= 1
        comps += 1
    lista[j] = v
    comps += p - j
    return comps
#%%
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
            #print("DEBUG: ", lista)
    return comp, reco
#%%

def merge_sort(lista, comps):
    """Ordena lista mediante el método merge sort.
       Pre: lista debe contener elementos comparables.
       Devuelve: una nueva lista ordenada."""
    if len(lista) < 2:
        lista_nueva = lista
    else:
        medio = len(lista) // 2
        izq = merge_sort(lista[:medio], comps)[0]
        der = merge_sort(lista[medio:], comps)[0]
        lista_nueva = merge(izq, der, comps = comps)
    return lista_nueva, comps

def merge(lista1, lista2, comps):
    """Intercala los elementos de lista1 y lista2 de forma ordenada.
       Pre: lista1 y lista2 deben estar ordenadas.
       Devuelve: una lista con los elementos de lista1 y lista2."""
    i, j = 0, 0
    resultado = []
    while(i < len(lista1) and j < len(lista2)):
        if (lista1[i] < lista2[j]):
            resultado.append(lista1[i])
            i += 1
            comps[0] += 1
        else:
            resultado.append(lista2[j])
            j += 1
            comps[0] += 1

    # Agregar lo que falta de una lista
    resultado += lista1[i:]
    resultado += lista2[j:]

    return resultado
#%%
def generar_lista(N):
    l = []
    for _ in range(N):
        value = random.randint(1, 1000)
        l.append(value)
    return l
#%%
comparaciones_seleccion = []
comparaciones_insercion = []
comparaciones_burbujeo = []
comparaciones_merge = []
#for i in range(100):
    #list = generar_lista(10)
    #a = list.copy()
    #comp_sele.append(ord_seleccion(a))
    #b = list.copy()
    #comp_ins.append(ord_insercion(b))
    #c = list.copy()
    #comp_bur.append(ord_burbujeo(c)[0])
    #print("DEBUG: ", list)
#print(f'El promedio de comparaciones con seleccion es {np.mean(comp_sele)}')
#print(f'El promedio de comparaciones con insercion es {np.mean(comp_ins)}')
#print(f'El promedio de comparaciones con burbujeo es {np.mean(comp_bur)}')
N = 1
while N < 257:
    listado = generar_lista(N)
    a = listado.copy()
    comparaciones_seleccion.append(ord_seleccion(a))
    b = listado.copy()
    comparaciones_insercion.append(ord_insercion(b))
    c = listado.copy()
    comparaciones_burbujeo.append(ord_burbujeo(c)[0])
    d = listado.copy()
    comparaciones_merge.append(merge_sort(d,[0])[1].pop())

    N += 1

rango = np.arange(1,257)

plt.plot(rango, comparaciones_seleccion, c='r', linestyle='-.', label='seleccion')
plt.plot(rango, comparaciones_insercion, c='b', label='insercion')
plt.plot(rango, comparaciones_burbujeo, c='g', label='burbujeo')
plt.plot(rango, comparaciones_merge, c='k', label='merge sort')
plt.ylim(0,60000)
plt.xlim(0,256)
plt.xlabel('Longitud de lista')
plt.ylabel('Nro de comparaciones')
plt.legend()
plt.title('Comparacion de algoritmos')
plt.show()