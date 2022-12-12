from collections import deque

#this program is a simple structure of a FIFO queue wherein you add another element to the last index then gets the first element from the left side
#or the one with zero index
class Queue: #object constructor
    #class is very useful to somehow make a local variable accessible to every defined functions
    def __init__(self, *elements): #__init__ is automatically used when creating a class; the asterisk beside the elements parameter allows you to provide varying number of positional arguments
        self._elements = deque(elements) #self parameter used to access variables of the class
    
    def __len__(self): # this reports the stack's number of elements
        """defining __len__ will make len() work since it calls upon __len__"""
        return len(self._elements)

    def __iter__(self): #this will make class instances usable/iterable through looping
        """"when iterating this will automatically dequeue elements"""
        while len(self) > 0:
            yield self.dequeue() #yield is similar to return statement but returns a generator object the one that calls the function

    def enqueue(self, element):
        self._elements.append(element) #the underscore on the elements means internal bit of implementation which means it cannot be accessed outside the class/modify
    
    def dequeue(self):
        return self._elements.popleft()#gets the first element from the left since this is portrayed in a horizontal manner but still preserves the general idea of a stack

fifo = Queue("1st", "2nd", "3rd") #added arguments to the class itself then transfers to the defined functions' parameter inside

#syntax to calling functions and adding value/argument to the parameter

len(fifo)

