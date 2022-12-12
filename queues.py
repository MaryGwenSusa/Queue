from collections import deque

class Queue: #object constructor
    """So class is very useful to somehow make a local variable accessible to every defined functions"""
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = deque() #self parameter used to access variables of the class
    
    def enqueue(self, element):
        self._elements.append(element)
    