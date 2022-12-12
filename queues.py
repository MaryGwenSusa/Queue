from collections import deque
from heapq import heappush, heappop
from queues import PriorityQueue
#heap compares elements by value not by priority so Python’s tuple can be used for comparison which takes into account the tuple’s components

#variables with value as argument for priority parameter
CRITICAL = 3
IMPORTANT = 2
NEUTRAL = 1

class PriorityQueue:
    def __init__(self): #__init__ is automatically used when creating a class
        self._elements = [] #self parameter used to access variables of the class; the underscore on the elements means internal bit of implementation which means it cannot be accessed outside the class/modify

    def enqueue_with_priority(self, priority, value):
        #Notice that the priority comes before the value to take advantage of how Python compares tuples
        heappush(self._elements, (priority, value)) #somehow works like .append()
        #the first element on a heap always has the smallest (min-heap) or the highest (max-heap) value, depending on how you define the condition for the mentioned relationship
        #lower Unicode means the element is smaller
    
    def dequeue(self):
        return heappop(self._elements) #When you pop an element from a heap, you’ll always get the first one, while the remaining elements might shuffle a little bit

messages = PriorityQueue()
messages.enqueue_with_priority(IMPORTANT, "Windshield wipers turned on")
messages.enqueue_with_priority(NEUTRAL, "Radio station tuned in")
messages.enqueue_with_priority(CRITICAL, "Brake pedal depressed")
messages.enqueue_with_priority(IMPORTANT, "Hazard lights turned on")

print(messages.dequeue())


#heap compares elements by value not by priority so Python’s tuple can be used for comparison which takes into account the tuple’s components
#fruits = []
#heappush(fruits, "orange") 
#heappush(fruits, "apple")
#heappush(fruits, "banana")

#print(fruits)
#lower Unicode means the element is smaller
#print(heappop(fruits))

#Notice how the banana and orange swapped places to ensure the first element continues to be the smallest
#print(fruits)
