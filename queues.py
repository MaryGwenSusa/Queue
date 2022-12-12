from collections import deque

class Queue: #object constructor
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = deque()