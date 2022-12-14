import argparse #makes it easy to write user-friendly command-line interfaces
from queue import LifoQueue, PriorityQueue, Queue
import threading
from random import choice, randint
from time import sleep
from itertools import zip_longest
from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel

#FIRST SYNCHRONIZED QUEUE, UNBOUNDED FIFO QUEUE

"""this dictionary maps queue names to their respective classes, which you call to create a new queue instance based on the value of a command-line argument"""
QUEUE_TYPES = {
    "fifo": Queue,
    "lifo": LifoQueue,
    "heap": PriorityQueue
}

"""producers will always push their finished products through the queue to the consumers. Even though it may sometimes appear as if a consumer takes an element directly from 
a producer, it’s only because things are happening too fast to notice the enqueue and dequeue operations"""
def main(args):
    """this function is the entry point which receives the parsed arguments (thru argparse module) supplied by parse_args()"""
    """the number of producers and consumers is determined by the command-line arguments passed into your function. They’ll begin working and using the queue for interthread 
    communication as soon as you start them."""
    buffer = QUEUE_TYPES[args.queue]()
    producers = [
        Producer(args.producer_speed, buffer, PRODUCTS)
        #for _ in range is used when there is no interest in values returned by a function--underscore in place of variable name. basically, there is no interest in how many 
        # times the loop is run, just that it should run some specific number of times overall
        for _ in range(args.producers)
    ]
    consumers = [
        Consumer(args.consumer_speed, buffer) for _ in range(args.consumers)
    ]

    for producer in producers:
        producer.start() #start() simply starts thread activity

    for consumer in consumers:
        consumer.start()
    
    view = View(buffer, producers, consumers) #view instance continually re-renders the screen to reflect the current state of your application
    view.animate() 


def parse_args():
    """this function supplies parsed arguments"""
    parser = argparse.ArgumentParser() #argparse.ArgumentParser() is a container for argument specifications and has options that apply the parser as whole
    parser.add_argument("-q", "--queue", choices=QUEUE_TYPES, default="fifo") #.add_argument method attaches individual argument specifications to the parser. It supports positional arguments, options that accept values, and on/off flags
    parser.add_argument("-p", "--producers", type=int, default=3)
    parser.add_argument("-c", "--consumers", type=int, default=2)
    parser.add_argument("-ps", "--producer-speed", type=int, default=1)
    parser.add_argument("-cs", "--consumer-speed", type=int, default=1)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt: #thrown when a user or programmer interrupts a program's usual execution
        pass

PRODUCTS = (
    ":balloon:",
    ":cookie:",
    ":crystal_ball:",
    ":diving_mask:",
    ":flashlight:",
    ":gem:",
    ":gift:",
    ":kite:",
    ":party_popper:",
    ":postal_horn:",
    ":ribbon:",
    ":rocket:",
    ":teddy_bear:",
    ":thread:",
    ":yo-yo:",
)


# producer and consumer threads will share a wealth of attributes and behaviors, which will be both encapsulated in Worker class
"""worker class will extend the threading.Thread class and configures itself as a daemon thread so that its instances won’t prevent the program from exiting when the main 
thread finishes (like when there's a keyboard interrupt)"""
class Worker(threading.Thread):
    def __init__(self, speed, buffer):
        #a worker object expects the speed rate to work with and a buffer queue to put finished products into or get them from
        super().__init__(daemon=True) #daemon means it runs as a background process
        self.speed = speed
        self.buffer = buffer
        self.product = None
        self.working = False
        self.progress = 0
    
    #@python decorator makes usage of getter and setters much easier in Object-Oriented Programming
    @property
    def state(self):
        """this method returns a string with either the product’s name and the progress of work or a generic message indicating that the worker is currently idle"""
        if self.working:
            return f"{self.product} ({self.progress}%)"
        return ":zzz: Idle"

    def simulate_idle(self):
        """this method resets the state of a worker thread and goes to sleep for a few randomly chosen seconds"""
        self.product = None
        self.working = False
        self.progress = 0
        sleep(randint(1, 3))

    def simulate_work(self):
        """this method picks a random delay in seconds (with the help of randint function) adjusted to the worker’s speed and progresses through the work"""
        self.working = True
        self.progress = 0
        delay = randint(1, 1 + 15 // self.speed) #makes sure the progress is somehow realistic
        for _ in range(100): #to progress to "100%" completeness
            sleep(delay / 100) #will make it appear as if it is loading
            self.progress += 1 #increment

"""this class will render the current state of producers, consumers, and the queue ten times a second"""
class View:
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers

    def animate(self):
        #with statement ensures proper acquisition and release of resources
        #screen=True will opt to show a Live display in the “alternate screen” upon setting it on the constructor. this will allow your live display to go full screen and restore the command prompt on exit
        #By default, the live display will refresh 4 times a second. the refresh rate can be with the refresh_per_second argument on the Live constructor
        """from rich module, live display is used to animate parts of the terminal"""
        with Live(
            self.render(), screen=True, refresh_per_second=10
        ) as live:
            while True:
                live.update(self.render()) #.update() is useful if the information to display is too dynamic to generate by updating a single renderable

    def render(self):
        #notice the use of structural pattern matching to set the title and products based on the queue type; match case statement in Python is more powerful and allows for 
        #more complicated pattern matching
        match self.buffer:
            case PriorityQueue():
                title = "Priority Queue"
                products = map(str, reversed(list(self.buffer.queue))) #map () returns a map object
            case LifoQueue():
                title = "Stack"
                products = list(self.buffer.queue)
            case Queue():
                title = "Queue"
                products = reversed(list(self.buffer.queue))
            case _: #equivalent to else in if-elif-else statement
                title = products = ""
        
        rows = [
            Panel(f"[bold]{title}:[/] {', '.join(products)}", width=82)
        ] #Panel(), from rich module, is a console renderable that draws aborder around its contents
        #zip_longest function (from iteratools module) falls under the category of Terminating Iterators. It prints the values of iterables alternatively in sequence. If one 
        # of the iterables is printed fully, the remaining values are filled by the values assigned to fillvalue parameter.
        pairs = zip_longest(self.producers, self.consumers) 
        for i, (producer, consumer) in enumerate(pairs, 1):
            left_panel = self.panel(producer, f"Producer {i}")
            right_panel = self.panel(consumer, f"Consumer {i}")
            rows.append(Columns([left_panel, right_panel], width=40)) #Columns(), from rich module, displays renderables in neat columns
        return Group(*rows) #Group(), from rich module, takes a group of renderables (group of rows in this case) and returns a renderable object that renders the group
    
    def panel(self, worker, title):
        """this method focuses on the alignment of the product and its 'progress'"""
        if worker is None:
            return ""
        padding = " " * int(29 / 100 * worker.progress)
        align = Align(
            padding + worker.state, align="left", vertical="middle"
        ) #Align function also from rich module aligns renderable by adding space if necessary
        return Panel(align, height=5, title=title)

class Producer(Worker):
    """producer thread will extend a Worker class and take an additional collection of products to choose from"""
    def __init__(self, speed, buffer, products):
        super().__init__(speed, buffer)
        self.products = products

    def run(self):
        """a producer works in an infinite loop, choosing a random product and simulating some work before putting that product onto the queue, called a buffer. It then 
         to sleep for a random period, and when it wakes up again, the process repeats"""
        while True:
            self.product = choice(self.products) #choice() method, from random module, returns a randomly selected element from the specified sequence
            self.simulate_work()
            self.buffer.put(self.product)
            self.simulate_idle()

class Consumer(Worker):
    """similar structure with Producer class but more straight-forward """
    def run(self):
        while True:
            #get() blocks by default, which will keep the consumer thread stopped and waiting until there’s at least one product in the queue. this way, a waiting consumer 
            # won’t be wasting any CPU cycles while the operating system allocates valuable resources to other threads doing useful work
            #to avoid a deadlock, you can optionally set a timeout on the .get() method by passing a timeout keyword argument with the number of seconds to wait before 
            # giving up
            #deadlock is a concurrency failure mode where a thread or threads wait for a condition that never occurs
            self.product = self.buffer.get() #get() method returns the value of the item in a dict with the specified key
            self.simulate_work()
            self.buffer.task_done() #task_done() marks the task as done
            self.simulate_idle()

#You can increase the number of producers, their speed, or both to see how these changes affect the overall capacity of your system. Because the queue is unbounded, 
# it’ll never slow down the producers. However, if you specified the queue’s maxsize parameter, then it would start blocking them until there was enough space in the 
# queue again.