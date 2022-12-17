import argparse
import asyncio
from collections import Counter
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import aiohttp
import sys
from typing import NamedTuple

async def main(args): #the syntax async def introduces either a native coroutine or an asynchronous generator. the expressions async with and async for are also valid
    session = aiohttp.ClientSession() #client session is the recommended interface for making HTTP requests. session encapsulates a connection pool (connector 
    #instance) and supports keepalives by default
    try: #the try block lets you test a block of code for errors
        links = Counter()
        display(links)
    finally: #finally block always gets executed either exception is generated or not
        await session.close() 
        #await passes function control back to the event loop (it suspends the execution of the surrounding coroutine)
        #close() method closes an open file. files should always be closed, in some cases, due to buffering, changes made to a file may not show until you
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

"""only returns the received content as long as it’s HTML, which you can tell by looking at the Content-Type HTTP header"""
async def fetch_html(session, url):
    """extracts links from the HTML content"""
    async with session.get(url) as response: #get() method returns the value for the given key if present in the dictionary. if not, then it will return None 
        #(if get() is used with only one argument)
        #the Response interface of the Fetch API represents the response to a request
        if response.ok and response.content_type == "text/html":
            #the ok read-only property of the Response interface contains a Boolean stating whether the response was successful 
            #the Content-Type representation header is used to indicate the original media type of the resource (prior to any content encoding applied for sending)
            return await response.text() #text() method of the Response interface takes a Response stream and reads it to completion. it returns a promise 
            #that resolves with a String. the response is always decoded using UTF-8.

def parse_links(url, html):
    """parses HTML links"""
    soup = BeautifulSoup(html, features="html.parser") #BeautifulSoup object represents the document as a nested data structure
    for anchor in soup.select("a[href]"): #.select(rlist, wlist, xlist[, timeout]): the first three arguments are iterables of ‘waitable objects’: either integers 
    #representing file descriptors or objects with a parameterless method named fileno() returning such an integer. rlist: wait until ready for reading
        href = anchor.get("href").lower()
        if not href.startswith("javascript:"): #skips inline JavaScript in the href attribute
            yield urljoin(url, href) #optionally join a relative path with the current URL to form an absolute interpretation of the latter

class Job(NamedTuple):
    #define a new data type representing a job to be put in the queue
    url: str
    depth: int = 1