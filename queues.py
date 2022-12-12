from collections import deque

class Queue: #object constructor
    """this program is a simple structure of a FIFO queue wherein you add another element to the last index then gets the first element from the left side"""
    #or the one with zero index
    #class is very useful to somehow make a local variable accessible to every defined functions
    def __init__(self, *elements): #__init__ is automatically used when creating a class; the asterisk beside the elements parameter allows you to provide varying number of positional arguments
        """here inputting initial elements is allowed"""
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

class Stack(Queue):
    """this program is a simple structure of a LIFO queue hwerein you add naother element to the last index then gets the last element you add first"""
    def dequeue(self):
        #return self._elements.popleft()#gets the first element from the left since this is portrayed in a horizontal manner but still preserves the general idea of a stack
        return self._elements.pop() #gets the last element

"""input initial elements"""
lifo = Stack("1st", "2nd", "3rd") #added arguments to the class itself then transfers to the defined functions' parameter inside

lifo.enqueue("4th") #syntax to calling functions and adding value/argument to the parameter
lifo.enqueue("5th")
lifo.enqueue("6th")


print(len(lifo))
print(lifo.__len__()) #another syntax to call the __len__ function inside the class and print its processed data

for element in lifo: #print in loop each element of the stack
    print(element)


print(len(lifo)) #since there's a function that automatically dequeues the elements, here is a proof of that

