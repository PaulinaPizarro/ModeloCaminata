import osmnx as ox

import networkx as nx

import geopandas as gpd

import matplotlib.pyplot as plt

import pandas as pd

import math

from operator import itemgetter

class Manzana:
    def __init__(self, id, lat, long, gen, atrac, pob, sub, dens):
        self.id = id
        self.lat = lat
        self.long = long
        self.gen = gen
        self.atrac = atrac
        self.pob = pob
        self.sub = sub
        self.dens = dens

## Cree una manzana 0 porque no sabia como empezar la clase nodo sin darle una manzana asignada, que se calcula despues
manzana0 = Manzana(0, 0, 0, 0, 0, 0, 0, 0)

class Nodo:
    def __init__(self, id, lat, long, x, y, gen, atrac, manzanas):
        self.id = id
        self.lat = lat
        self.long = long
        self.x = x
        self.y = y
        self.gen = gen
        self.atrac = atrac
        self.manzanas = manzanas

def genera_red():
    graph = ox.graph_from_bbox(20.706, 20.67, -103.335, -103.358, network_type='walk')
    edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
    graph_proj = ox.project_graph(graph)
    return(graph_proj)

def mostrar_red(graph):
    fig, ax = ox.plot_graph(graph)
    plt.tight_layout()

def instanciar_nodos(graph_proj):
    lista_nodos = []
    for val in graph_proj.nodes.items():
        id = val[0]
        for v in val[1].items():
            if v[0] == 'x':
                x = v[1]
            elif v[0] == 'y':
                y = v[1]
            elif v[0] == 'lon':
                long = v[1]
            elif v[0] == 'lat':
                lat = v[1]
        nodo = Nodo(id, lat, long, x, y, 0, 0, [manzana0, manzana0, manzana0, manzana0])
        lista_nodos.append(nodo)
    lista_nodos.sort(key=itemgetter("id"))
    #i = 1
    #for nodo in lista_nodos:
    #	nodo.id = i
    #	i += 1
    return(lista_nodos)



def instanciar_manzanas(archivo):
    archivo_manzanas = open(archivo + ".csv", "r")
    lista_manzanas = []
    for l in archivo_manzanas:
        linea = l.split(",")
        if linea[1] != "SUP":
            pob = float(linea[0])
            sup = float(linea[1])
            dens = float(linea[2])
            x = float(linea[3])
            y = float(linea[4])
            id = int(linea[5])
            lat = float(linea[6])
            lon = float(linea[7].strip())
            manzana_aux = Manzana(id, lat, long, 0, 0, pob, sup, dens)
            lista_manzanas.append(manzana_aux)
    return(lista_manzanas)

def show_nodo(lista_nodos):
    print("Nodos")
    for n in lista_nodos:
        manz = n.manzana
        print(n.id, n.lat, n.long, n.x, n.y, n.gen, n.atrac, manz[0].id, manz[1].id, manz[2].id, manz[3].id)

# Pitagoras
def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distancia

def ordenar_diccionario1(dicc):
    matriz = []
    for i in dicc:
        origen = i[0]
        dict = i[1]
        list = []
        for destino, distancia in dict.items():
            temp = [destino, distancia]
            list.append(temp)
        list.sort(key=lambda x: x[0])
        matriz.append([origen, list])
    matriz.sort(key=lambda x: x[0])
    return (matriz)


def ordenar_diccionario2(dicc):
    matriz = []
    for key, value in dicc.items():
        origen = key
        list = []
        for destino, ruta in value.items():
            temp = [destino, ruta]
            list.append(temp)
        list.sort(key=lambda x: x[0])
        matriz.append([origen, list])
    matriz.sort(key=lambda x: x[0])
    return (matriz)


def matriz_a_txt(matriz, nombre):
    new_matriz = []
    for i in matriz:
        lista = []
        for j in i[1]:
            lista.append(j[1])
        new_matriz.append(lista)
    with open(nombre + '.txt', 'w') as f:
        for item in new_matriz:
            f.write("%s\n" % item)
    f.close()

def asignar_manz_a_nodo(lista_nodos, lista_manzanas):
    for n in lista_nodos:
        distancia_min = 9999999999999999999
        list_dist_min = [[distancia_min, manzana0], [distancia_min, manzana0], [distancia_min, manzana0], [distancia_min, manzana0]]
        for manzana in lista_manzanas:
            punto1 = (manzana.lat, manzana.long)
            punto2 = (n.lat, n.long)
            distancia = calcular_distancia(punto1, punto2)
            if distancia < list_dist_min[3][0]:
                list_dist_min[3] = distancia, manzana
                list_dist_min.sort(key=lambda x: x[0])
        manz_cercanas = [list_dist_min[0][1], list_dist_min[1][1], list_dist_min[2][1], list_dist_min[3][1]]
        n.manzana = manz_cercanas
    return(lista_nodos)

#Libreria que genera diccioanrio ruta y distancia'
def diccionarios_ruta_min(graph_proj):
    ruta = nx.shortest_path(G= graph_proj, source=None, target=None, weight='length')
    distancia = nx.shortest_path_length(G= graph_proj, source=None, target=None, weight='length')
    return ruta, distancia


def cargar_arcos(grafo, lista_secuencia, flujo):
    grafo.add_path(lista_secuencia)
    i = 0
    while i < len(lista_secuencia)-1:
        grafo[lista_secuencia[i]][lista_secuencia[i+1]]['weight'] = flujo
        i += 1





G = nx.read_gpickle("test.gpickle")

ruta, distancia = diccionarios_ruta_min(G)




for i in G.get_edge_data(1597308934, 1597308938):
    print(i)

print(type(ruta))
1597308934
1597308938