from collections import deque

#this program is a simple structure of a FIFO queue wherein you add another element to the last index then gets the first element from the left side
#or the one with zero index
class Queue: #object constructor
    #class is very useful to somehow make a local variable accessible to every defined functions
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = deque() #self parameter used to access variables of the class
    
    def enqueue(self, element):
        self._elements.append(element) #the underscore on the elements means internal bit of implementation which means it cannot be accessed outside the class/modify
    
    def dequeue(self):
        return self._elements.popleft()#gets the first element from the left since this is portrayed in a horizontal manner but still preserves the general idea of a stack

        