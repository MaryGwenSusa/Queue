import os
os.add_dll_directory("C:/Program Files/Graphviz/bin")
import pygraphviz as pgv
import networkx as nx
graph = nx.nx_agraph.read_dot("roadmap.dot")
print(graph.nodes["london"]) #search up node with matching element value and take all of its value/element or associated dictionary of attributes
{'country': 'England',
 'latitude': '51.507222',
 'longitude': '-0.1275',
 'pos': '80,21!', #center of node after applying Mercator projection which is a cylindrical map projection, the standard dince it represents north as up and south as down everywhere while preserving local directions and shapes
 'xlabel': 'City of London',
 'year': 0} #corresponds to when a city got its status; when 0 = time immemorial