import networkx as nx
from graph import City, load_graph, dijkstra_shortest_path

nodes, graph = load_graph("roadmap.dot", City.from_dict)

city1 = nodes["london"]
city2 = nodes["edinburgh"]

def distance(weights):
    """defined a concrete strategy that produces a floating-point distance based on the input dictionary"""
    return float(weights["distance"])