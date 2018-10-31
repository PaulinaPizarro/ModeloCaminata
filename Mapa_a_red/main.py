import osmnx as ox

import networkx as nx

import geopandas as gpd

import matplotlib.pyplot as plt

import pandas as pd


class Manzana:
    def __init__(self, id, lat, long, gen, atrac):
        self.id = id
        self.lat = lat
        self.long = long
        self.gen = gen
        self.atrac = atrac
## Cree una manzana 0 porque no sabia como empezar la clase nodo sin darle una manzana asignada, que se calcula despues
manzana0 = Manzana(0,0,0,0,0)

class Nodo:
    def __init__(self, id, lat, long, x, y, gen, atrac, manzanas):
        self.id = id
        self.lat = lat
        self.long = long
        self.x = x
        self.y= y
        self.gen = gen
        self.atrac = atrac
        self.manzanas = manzanas

# Pitagoras
def calcular_distancia(punto1, punto2):
    x1,y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x1-x2)^2 +(y1-y2)^2)
    return distancia
  
 
## Genera la red
center_point_santuario = (20.684851, -103.347916)
#graph = ox.graph_from_place(place_name, network_type='walk')
graph = ox.graph_from_point(center_point_santuario, distance=1000, distance_type='bbox',
                     network_type='walk')
#fig, ax = ox.plot_graph(graph)
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

###Esto proyecta el grafo en otro tipo de coordenadas
graph_proj = ox.project_graph(graph)
#fig, ax = ox.plot_graph(graph_proj)
#plt.tight_layout()

# ahora empiezo a instanciar los nodos

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


#shortest path

##los nodos orig y target hay que definirlos
#orig_node = (orig_point.y, orig_point.x)
#target_node = (target_point.y, target_point.x)
#route = nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight='length')

#print(route)
#fig, ax = ox.plot_graph_route(graph_proj, route, origin_point=orig_xy, destination_point=target_xy)

#plt.tight_layout()
