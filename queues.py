from heapq import heappush
#the first element on a heap always has the smallest (min-heap) or the highest (max-heap) value, depending on how you define the condition for the mentioned relationship
#When you pop an element from a heap, you’ll always get the first one, while the remaining elements might shuffle a little bit
fruits = []
heappush(fruits, "orange") #somehow works like .append()
heappush(fruits, "apple")
heappush(fruits, "banana")

print(fruits)
