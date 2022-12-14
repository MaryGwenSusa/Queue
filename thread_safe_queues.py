import argparse
from queue import LifoQueue, PriorityQueue, Queue

"""this dictionary maps queue names to their respective classes, which you call to create a new queue instance based on the value of a command-line argument"""
QUEUE_TYPES = {
    "fifo": Queue,
    "lifo": LifoQueue,
    "heap": PriorityQueue
}

def main(args):
    """this function is the entry point which receives the parsed arguments supplied by parse_args()"""
    buffer = QUEUE_TYPES[args.queue]()