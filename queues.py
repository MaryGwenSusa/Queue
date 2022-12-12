from heapq import heappush, heappop
#heap compares elements by value not by priority so Python’s tuple can be used for comparison which takes into account the tuple’s components
#the first element on a heap always has the smallest (min-heap) or the highest (max-heap) value, depending on how you define the condition for the mentioned relationship
fruits = []
heappush(fruits, "orange") #somehow works like .append()
heappush(fruits, "apple")
heappush(fruits, "banana")

print(fruits)
#lower Unicode means the element is smaller
#When you pop an element from a heap, you’ll always get the first one, while the remaining elements might shuffle a little bit
print(heappop(fruits))

#Notice how the banana and orange swapped places to ensure the first element continues to be the smallest
print(fruits)

person1 = ("John", "Doe", 42)
person2 = ("John", "Doe", 42)
person3 = ("John", "Doe", 24)

if person1 < person2:
    print(True)
else:
    print(False)
if person2 < person3:
    print(True)
else:
    print(False)
