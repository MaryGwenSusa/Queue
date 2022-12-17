import argparse
import asyncio
from collections import Counter

import aiohttp

async def main(args): #the syntax async def introduces either a native coroutine or an asynchronous generator. the expressions async with and async for are also valid
    session = aiohttp.ClientSession() #client session is the recommended interface for making HTTP requests. session encapsulates a connection pool (connector 
    #instance) and supports keepalives by default
    try: #the try block lets you test a block of code for errors
        links = Counter()
        display(links)
    finally: #finally block always gets executed either exception is generated or not
        await session.close() 
        #await passes function control back to the event loop (it suspends the execution of the surrounding coroutine)
        #Tclose() method closes an open file. files should always be closed, in some cases, due to buffering, changes made to a file may not show until you
        #close the file

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-d", "--max-depth", type=int, default=2)
    parser.add_argument("-w", "--num-workers", type=int, default=3)
    return parser.parse_args() #parse_args will take the arguments you provide on the command line when you run your program and interpret them according to the 
    #arguments you have added to your ArgumentParser object

def display(links):
    """this coroutine displays the list of links sorted by the number of visits in descending order"""
    for url, count in links.most_common():
        print(f"{count:>3} {url}")

if __name__ == "__main__":
    #executes main() coroutine on the default event loop
    asyncio.run(main(parse_args())) #the asyncio.run() function to run the top-level entry point “main()” function
