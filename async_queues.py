import argparse
import asyncio
from collections import Counter

import aiohttp

async def main(args): #the syntax async def introduces either a native coroutine or an asynchronous generator. the expressions async with and async for are also valid
    session = aiohttp.ClientSession() #client session is the recommended interface for making HTTP requests. session encapsulates a connection pool (connector 
    #instance) and supports keepalives by default