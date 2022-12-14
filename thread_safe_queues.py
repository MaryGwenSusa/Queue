import argparse #makes it easy to write user-friendly command-line interfaces
from queue import LifoQueue, PriorityQueue, Queue
import threading
from random import randint
from time import sleep

"""this dictionary maps queue names to their respective classes, which you call to create a new queue instance based on the value of a command-line argument"""
QUEUE_TYPES = {
    "fifo": Queue,
    "lifo": LifoQueue,
    "heap": PriorityQueue
}

def main(args):
    """this function is the entry point which receives the parsed arguments (thru argparse module) supplied by parse_args()"""
    buffer = QUEUE_TYPES[args.queue]()

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