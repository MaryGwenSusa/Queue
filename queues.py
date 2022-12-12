from collections import deque

class Queue: #object constructor
    """So class is very useful to somehow make a local variable accessible to every defined functions"""
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = deque() #self parameter used to access variables of the class
    
    def enqueue(self, element):
        self._elements.append(element)
    
    def dequeue(self):
        return self._element.popleft()#gets the first element from the left since this is portrayed in a horizontal manner but still preserves the general idea of a stack

        