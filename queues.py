from collections import deque
from heapq import heappush, heappop

class PriorityQueue:
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = [] #self parameter used to access variables of the class; the underscore on the elements means internal bit of implementation which means it cannot be accessed outside the class/modify








#heap compares elements by value not by priority so Python’s tuple can be used for comparison which takes into account the tuple’s components
#the first element on a heap always has the smallest (min-heap) or the highest (max-heap) value, depending on how you define the condition for the mentioned relationship
#fruits = []
#heappush(fruits, "orange") #somehow works like .append()
#heappush(fruits, "apple")
#heappush(fruits, "banana")

#print(fruits)
#lower Unicode means the element is smaller
#When you pop an element from a heap, you’ll always get the first one, while the remaining elements might shuffle a little bit
#print(heappop(fruits))

#Notice how the banana and orange swapped places to ensure the first element continues to be the smallest
#print(fruits)
