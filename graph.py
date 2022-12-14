from typing import NamedTuple
from math import inf as infinity
from queues import MutableMinHeap
import networkx as nx
from collections import deque

class IterableMixin: #inclusion of a mixin class rather than pure inheritance
    #mixins are great for encapsulating behavior rather than state
    #by composing a class with one or more mixins, you can change or augment its original behavior.
    def __len__(self): # this reports the stack's number of elements
        """defining __len__ will make len() work since it calls upon __len__"""
        return len(self._elements)
    
    def __iter__(self): ##this will make class instances usable/iterable through looping
        """"when iterating this will automatically dequeue elements"""
        while len(self) > 0:
            yield self.dequeue() #yield is similar to return statement but returns a generator object the one that calls the function

class Queue(IterableMixin): #object constructor
    """this class is a simple structure of a FIFO queue wherein you add another element to the last index then gets the first element from the left side 
    or the one with zero index"""
    def __init__(self, *elements):
        """here inputting initial elements is allowed"""
        self._elements = deque(elements)

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()
        
class Stack(Queue):
    """this program is a simple structure of a LIFO queue wherein you add naother element to the last index then gets the last element you add first"""
    def dequeue(self):
        # this was for the FIFO -- return self._elements.popleft() #gets the first element from the left since this is portrayed in a horizontal manner but still preserves 
        # the general idea of a stack
        return self._elements.pop() #gets the last element

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
    """helper function that returns a list of neighbors and their weights sorted by taking the dictionary of all the weights associated with an edge and 
    returns a sorting key."""
    return sorted(neighbors.items(), key=lambda item: strategy(item[1])) #.items() used to return the list with all dictionary keys with values

def by_distance(weights):
    """defined a concrete strategy that produces a floating-point distance based on the input dictionary"""
    return float(weights["distance"])

"""identify the immediate neighbors in the purpose of looking for the shortest path/finding available routes"""
#for neighbor, weights in sort_by(graph[nodes["london"]], by_distance): 
"""an iteration over the neighbors of "London", sorted by distance in ascending order"""
    # accessing the distance element attributes will process the possible weights of the connecting edges, such as distances or the estimated travel times, 
    # and reveal it numerically which is needed as a basis for the best path
    #print(f"{weights['distance']:>3} miles, {neighbor.name}")


"""this defined function takes another node as an argument and optionally lets you order the neighbors using a custom strategy"""
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
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited: #if statement to mark visited nodes by adding them to a Python set, so that each neighbor is visited at most once
                visited.add(neighbor)
                queue.enqueue(neighbor)

def breadth_first_search(graph, source, predicate, order_by=None):
    return search(breadth_first_traverse, graph, source, predicate, order_by)

#won't initially mark the source node as visited
def depth_first_traverse(graph, source, order_by=None):
    stack = Stack(source)
    #visited nodes are initialized to an empty set before popping elements from the stack 
    visited = set() #set() is used to convert any of the iterable to sequence of iterable elements with distinct elements
    while stack:
        #checks if the node was already visited much earlier than in the breadth-first traversal
        if (node := stack.dequeue()) not in visited:
            yield node
            visited.add(node)
            neighbors = list(graph.neighbors(node))
            if order_by:
                neighbors.sort(key=order_by)
            for neighbor in reversed(neighbors): #LIFO queue
                """this won't mark the neighbors as visited immediately after pushing them onto the stack, unlike, in the breadth-first-t structure 
                which is this:
                for neighbor in neighbors:
                    if neighbor not in visited: #if statement to mark visited nodes by adding them to a Python set, so that each neighbor is visited at most once
                        visited.add(neighbor)
                        queue.enqueue(neighbor)
                """
                stack.enqueue(neighbor)

# call stack saved for backtracking and rewritten the function recursively
def recursive_depth_first_traverse(graph, source, order_by=None):
    visited = set()
    """avoid maintaining a stack of your own, as Python pushes each function call on a stack behind the scenes"""
    def visit(node): #only need to keep track of the visited nodes
        yield node
        visited.add(node)
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors: #no need to reverse the neighbors when iterating over them
            if neighbor not in visited:
                yield from visit(neighbor) #doesn't push already visited neighbors onto the stack

    return visit(source) #pops one when the corresponding function returns

def depth_first_search(graph, source, predicate, order_by=None):
    return search(depth_first_traverse, graph, source, predicate, order_by)

def search(traverse, graph, source, predicate, order_by=None):
    """called by breadth_first_search and depth_first_search looping over the yielded nodes (using for loop), and stops once the current node meets the expected criteria (thru if 
    statement); then, returns it"""
    for node in traverse(graph, source, order_by): 
        if predicate(node):
            return node

def dijkstra_shortest_path(graph, source, destination, weight_factory):
    previous = {}
    visited = set()

    unvisited = MutableMinHeap()
    """Initially, the distance to all destination cities is unknown, so an infinite cost should be assigned to each unvisited city except for the source, which has a distance 
    equal to zero"""
    for node in graph.nodes:
        unvisited[node] = infinity
    unvisited[source] = 0

    while unvisited:
        visited.add(node := unvisited.dequeue())
        for neighbor, weights in graph[node].items():
            """When a cheaper path to a neighbor is found, this if condition statement will update its total distance from the source in the priority queue, which rebalances 
            itself so that an unvisited node with the shortest distance will pop up first next time"""
            if neighbor not in visited:
                weight = weight_factory(weights)
                new_distance = unvisited[node] + weight
                if new_distance < unvisited[neighbor]:
                    unvisited[neighbor] = new_distance
                    previous[neighbor] = node
    
    return retrace(previous, source, destination)

#for city in depth_first_traverse(graph, nodes["edinburgh"]):
#    print(city.name)

