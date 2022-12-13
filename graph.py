from typing import NamedTuple
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

nodes, graph = load_graph("roadmap.dot", City.from_dict) #called the function with value arguments then stored in variables

def sort_by(neighbors, strategy):
    """helper function that returns a list of neighbors and their weights sorted by the specified strategy""""
    return sorted(neighbors.items(), key=lambda item: strategy(item[1]))

"""identify the immediate neighbors in the purpose of looking for the shortest path/finding available routes"""
for neighbor, weights in graph[nodes["london"]].items(): #.items() used to return the list with all dictionary keys with values
    # accessing the distance element attributes will process the possible weights of the connecting edges, such as distances or the estimated travel times, 
    # and reveal it numerically which is needed as a basis for the best path
    print(weights["distance"], neighbor.name)


    