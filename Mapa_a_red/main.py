import osmnx as ox

import networkx as nx

import geopandas as gpd

import matplotlib.pyplot as plt

import pandas as pd


center_point_santuario = (20.684851, -103.347916)

#graph = ox.graph_from_place(place_name, network_type='walk')

graph = ox.graph_from_point(center_point_santuario, distance=1000, distance_type='bbox',
                     network_type='walk')

#fig, ax = ox.plot_graph(graph)

edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
print(edges.columns)

graph_proj = ox.project_graph(graph)

#fig, ax = ox.plot_graph(graph_proj)

#plt.tight_layout()
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
print("Coordinate system:", edges_proj.crs)
print(edges_proj.head())
print(edges_proj.bounds.head())

#shortest path
from shapely.geometry import box
bbox = box(*edges_proj.unary_union.bounds)
print(bbox)
orig_point = bbox.centroid
print(orig_point)
nodes_proj['x'] = nodes_proj.x.astype(float)
maxx = nodes_proj['x'].max()
target_loc = nodes_proj.loc[nodes_proj['x']==maxx, :]
print(target_loc)

target_point = target_loc.geometry.values[0]

print(target_point)

orig_xy = (orig_point.y, orig_point.x)

target_xy = (target_point.y, target_point.x)

orig_node = ox.get_nearest_node(graph_proj, orig_xy, method='euclidean')

target_node = ox.get_nearest_node(graph_proj, target_xy, method='euclidean')

o_closest = nodes_proj.loc[orig_node]

t_closest = nodes_proj.loc[target_node]

print(orig_node)

print(target_node)

od_nodes = gpd.GeoDataFrame([o_closest, t_closest], geometry='geometry', crs=nodes_proj.crs)
route = nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight='length')

print(route)
fig, ax = ox.plot_graph_route(graph_proj, route, origin_point=orig_xy, destination_point=target_xy)

plt.tight_layout()