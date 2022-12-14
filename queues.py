from collections import deque
from typing import Any
#counts from zero to infinity concisely
from itertools import count
#lexicographic order - the alphabetical order of the dictionaries to sequences of ordered symbols or, more generally, of elements of a totally ordered set
from dataclasses import dataclass 
from heapq import heapify, heappush, heappop
#from queues import PriorityQueue
#heap compares elements by value not by priority so Python’s tuple can be used for comparison which takes into account the tuple’s components
"""This current program actually just has a problem with numerical value and turns out there are a lot of ways to fix this"""
#variables with value as argument for priority parameter
CRITICAL = 3
IMPORTANT = 2
NEUTRAL = 1

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

class PriorityQueue(IterableMixin):
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = [] #self parameter used to access variables of the class; the underscore on the elements means internal bit of implementation which means it cannot be accessed outside the class/modify
        self._counter = count() #generates consecutive data points usually used in maps

    def enqueue_with_priority(self, priority, value):
        element = (-priority, next(self._counter), value) #next() function returns the next item in an iterator.
        #Notice that the priority comes before the value to take advantage of how Python compares tuples
        heappush(self._elements, (element)) #somehow works like .append()
        #the first element on a heap always has the smallest (min-heap) or the highest (max-heap) value, depending on how you define the condition for the mentioned relationship
        #to fix that a negative sign is planted onto the priority variable so the highest value becomes the lowest
        #lower Unicode means the element is smaller
    
    def dequeue(self):
        return heappop(self._elements)[-1] #When you pop an element from a heap, you’ll always get the first one, while the remaining elements might shuffle a little bit
        #since there are three components inside the tuple--when performing a dequeue operation, you’ll unpack the value from the tuple by accessing its third component, 
        # located at index two. it would be safer to use the -1 to indicate the last component regardless of the number of components in the tuple--using the square bracket ([]) syntax 

"""this specialized priority queue stores data class elements instead of tuples because the elements must be mutable. Notice the additional order flag, which makes the elements comparable,
 just like tuples:"""
@dataclass(order=True) 
class Element:
    priority: float
    count: int
    value: Any

messages = PriorityQueue() #called the class
messages.enqueue_with_priority(IMPORTANT, "Windshield wipers turned on") #syntax to calling functions and adding value/argument to the parameter
messages.enqueue_with_priority(NEUTRAL, "Radio station tuned in")
messages.enqueue_with_priority(CRITICAL, "Brake pedal depressed")
messages.enqueue_with_priority(IMPORTANT, "Hazard lights turned on")

#print(messages.dequeue())
#print(messages.dequeue())
#print(messages.dequeue())
#print(messages.dequeue())

#@dataclass #used to represent messages in the queue; more convenient than strings but aren't comparable
#class Message:
#    event: str

#wipers = Message("Windshield wipers turned on")
#hazard_lights = Message("Hazard lights turned on")

#messages.enqueue_with_priority(CRITICAL, Message("ABS engaged"))

