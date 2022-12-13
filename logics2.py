import networkx as nx
from typing import NamedTuple
from collections import deque
from queues import Queue




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

def shortest_path(graph, source, destination, order_by=None):
    """Uses FIFO queue to keep track of the node neighbors"""
    queue = Queue(source)
    visited = {source}
    previous = {}
    #for node in queue:
    #   yield node
    """"the for loop can be used since there is a custom queue structure before that is iterable by dequeueing elements but it relies on a non-obvious implementation detail 
    in the Queue class--making the while loop with walrus operator to yield a dequeued node is more conventional"""
    while queue:
        #yield is similar to return statement but returns a generator object the one that calls the function
        node = queue.dequeue() #syntax := or walrus opearator assigns values to variables as part of a larger expression
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited: #if statement to mark visited nodes by adding them to a Python set, so that each neighbor is visited at most once
                visited.add(neighbor)
                queue.enqueue(neighbor)
                previous[neighbor] = node #populates dict of visited neighbors by associating it with previous nodes on the path
                if neighbor == destination:
                    return retrace(previous, source, destination)

def retrace(previous, source, destination):
    """iteratively looks up the dictionary built earlier when traversing the graph with the breadth-first approach"""
    path = deque() #called a double-ended queue

    current = destination
    """At each iteration, you add the current node to the path and move to the previous node. It will loop until the source is reached or in other case, 
    there isn't a source"""
    while current != source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None
    
    path.appendleft(source)
    return list(path)

def by_latitude(city):
    return -city.latitude #to enforce a descending order, the minus sign (-) is added in front of the .latitude attribute

def connected(graph, source, destination):
    """this will tell if certain cities may be connected or not: case in point, islands"""
    return shortest_path(graph, source, destination) is not None

nodes, graph = load_graph("roadmap.dot", City.from_dict) #called the function with value arguments then stored in variables

city1 = nodes["aberdeen"]
city2 = nodes["perth"]


"""when visiting a code, this will keep track of the previous node that led you to it by saving this information as a key-value pair in a dictionary"""
#for i, path in enumerate(nx.all_shortest_paths(graph, city1, city2), 1): #enumerate function takes a collectiona and returns objects
    #print(f"{i}.", " → ".join(city.name for city in path)) #.join function takes all items in an iterable and joins them into one string

"""queue-based implementation of shortest path will give the same results from networkx

this follows natural order of neighbors from the DOT file"""
#print(" → ".join(city.name for city in shortest_path(graph, city1, city2)))

"""prefers neighbors with a higher latitude, which you specify through a custom sort strategy"""
print(" → ".join(city.name for city in shortest_path(graph, city1, city2, by_latitude)))