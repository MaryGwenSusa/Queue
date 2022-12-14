import networkx as nx
#allows you to access Switch-specific elements such as buttons, filesystem, etc. via a high-level, object-oriented wrapper around libnx
from graph import City, load_graph, dijkstra_shortest_path

nodes, graph = load_graph("roadmap.dot", City.from_dict)

city1 = nodes["london"]
city2 = nodes["edinburgh"]

def distance(weights):
    """defined a concrete strategy that produces a floating-point distance based on the input dictionary"""
    return float(weights["distance"])

#for city in dijkstra_shortest_path(graph, city1, city2, distance):
#    print(city.name)

def weight(node1, node2, weights):
    return distance(weights)

for city in nx.dijkstra_path(graph, city1, city2, weight):
    print(city.name)