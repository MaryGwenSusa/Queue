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

from typing import NamedTuple
from queues import Queue
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

def breadth_first_traverse(graph, source, order_by=None):
    """Uses FIFO queue to keep track of the node neighbors"""
    queue = Queue(source)
    visited = {source}
    #for node in queue:
    #   yield node
    """"the for loop can be used since there is a custom queue structure before that is iterable by dequeueing elements but it relies on a non-obvious implementation detail 
    in the Queue class--making the while loop with walrus operator to yield a dequeued node is more conventional"""
    while queue:
        #yield is similar to return statement but returns a generator object the one that calls the function
        yield (node := queue.dequeue()) #syntax := or walrus opearator assigns values to variables as part of a larger expression
        for neighbor in graph.neighbors(node):
            if neighbor not in visited: #if statement to mark visited nodes by adding them to a Python set, so that each neighbor is visited at most once
                visited.add(neighbor)
                queue.enqueue(neighbor)

"""However, a flaw is found that the functions dont't allow sorting the neighbors in a particular order"""
def breadth_first_search(graph, source, predicate):
    """"This builds on top breadth_first_traverse by looping over the yielded nodes (using for loop), and stops once the current node meets the expected criteria (thru if 
    statement); then, returns it"""
    for node in breadth_first_traverse(graph, source):
        if predicate(node):
            return node
    

def is_twentieth_century(city):
    """defined a function that returns only qualified node from the boolean conditions of the target year"""
    return city.year and 1901 <= city.year <= 2000

#def order(neighbors):
    """order() wraps a list of sorted neighbors in a call to iter(). it’s because nx.bfs_tree() expects an iterator object as input for its sort_neighbors argument"""
    def by_latitude(city):
        return city.latitude
    return iter(sorted(neighbors, key=by_latitude, reverse=True)) #iterates the sorted neighbors of a certain node according to their latitude
    # iter () converts an iterable to the iterator

nodes, graph = load_graph("roadmap.dot", City.from_dict) #called the function with value arguments then stored in variables
#for node in nx.bfs_tree(graph, nodes["edinburgh"], sort_neighbors=order): #breadth-first search algorithm looks for a node that satisfies a particular condition by exploring the graph in concentric layers or levels
    #print("📍", node.name)
    #if is_twentieth_century(node.year):
        #print("Found:", node.name, node.year)
        #break

#else:
    #print("Not found")

#city = breadth_first_search(graph, nodes["edinburgh"], is_twentieth_century)
#print(city.name)


for city in breadth_first_traverse(graph, nodes["edinburgh"]):
    print(city.name)

#works exactly like this in the first attempt with netwrokx but the former fits perfectly with the current dataset:
#for neighbor in graph.neighbors(nodes["london"]):
    #print(neighbor.name)
    
