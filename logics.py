#import os
#os.add_dll_directory("C:/Program Files/Graphviz/bin")
#import pygraphviz as pgv
#import networkx as nx
#graph = nx.nx_agraph.read_dot("roadmap.dot")
#print(graph.nodes["london"]) #search up node with matching element value and take all of its value/element or associated dictionary of attributes
#{'country': 'England',
# 'latitude': '51.507222',
# 'longitude': '-0.1275',
# 'pos': '80,21!', #center of node after applying Mercator projection which is a cylindrical map projection, the standard dince it represents north as up and south as down everywhere while preserving local directions and shapes
# 'xlabel': 'City of London',
# 'year': 0} #corresponds to when a city got its status; when 0 = time immemorial


import networkx as nx

class City(NamedTuple): #extend a named tuple to ensure that your node objects are hashable, which is required by networkx; could also use a properly configured data class
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, attrs):
        "this will take a dictionary of attributes extracted from a DOT file and returns a new instance of the City class"
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"]),
        )

def load_graph(filename, node_factory): #callable factory for the node objects like from the City.from_dict() class method
    graph = nx.nx_agraph.read_dot(filename) #Reads a DOT file
    #build a mapping of node identifiers to the object-oriented representation of the graph nodes 
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data=True)
    }
    #returns the mapping and a new graph comprising nodes and weighted edges
    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data=True)
    )

def is_twentieth_century(year):
    """defined a function that returns only qualified node from the boolean conditions of the target year"""
    return year and 1901 <= year <= 2000

nodes, graph = load_graph("roadmap.dot", City.from_dict) #called the function with value arguments then stored in variables
for node in nx.bfs_tree(graph, nodes["edinburgh"]): #breadth-first search algorithm looks for a node that satisfies a particular condition by exploring the graph in concentric layers or levels
    print("📍", node.name)
    if is_twentieth_century(node.year):
        print("Found:", node.name, node.year)
        break

else:
    print("Not found")
