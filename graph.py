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
    