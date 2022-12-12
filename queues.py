from collections import deque
#counts from zero to infinity concisely
from itertools import count
#lexicographic order - the alphabetical order of the dictionaries to sequences of ordered symbols or, more generally, of elements of a totally ordered set
from dataclasses import dataclass 
from heapq import heappush, heappop
#from queues import PriorityQueue
#heap compares elements by value not by priority so Python’s tuple can be used for comparison which takes into account the tuple’s components
"""This current program actually just has a problem with numerical value and turns out there are a lot of ways to fix this"""
#variables with value as argument for priority parameter
CRITICAL = 3
IMPORTANT = 2
NEUTRAL = 1

class IterableMixin:
    def __len__(self): # this reports the stack's number of elements
        """defining __len__ will make len() work since it calls upon __len__"""
        return len(self._elements)
    
    def __iter__(self): ##this will make class instances usable/iterable through looping
        """"when iterating this will automatically dequeue elements"""
        while len(self) > 0:
            yield self.dequeue() #yield is similar to return statement but returns a generator object the one that calls the function

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
        
messages = PriorityQueue() #called the class
messages.enqueue_with_priority(IMPORTANT, "Windshield wipers turned on") #syntax to calling functions and adding value/argument to the parameter
messages.enqueue_with_priority(NEUTRAL, "Radio station tuned in")
messages.enqueue_with_priority(CRITICAL, "Brake pedal depressed")
messages.enqueue_with_priority(IMPORTANT, "Hazard lights turned on")

#print(messages.dequeue())
#print(messages.dequeue())
#print(messages.dequeue())
#print(messages.dequeue())


@dataclass #used to represent messages in the queue; more convenient than strings but aren't comparable
class Message:
    event: str

wipers = Message("Windshield wipers turned on")
hazard_lights = Message("Hazard lights turned on")

messages.enqueue_with_priority(CRITICAL, Message("ABS engaged"))




#Notice how the banana and orange swapped places to ensure the first element continues to be the smallest
#print(fruits)
