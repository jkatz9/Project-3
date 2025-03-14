import requests
import json
import pandas as pd
import sqlalchemy
import sqlite3
from pprint import pprint
import os
import sys
import time
import asyncio
import aiohttp
import json
import nest_asyncio

base_url = "https://api.openalex.org/"
email = "jukatz93@gmail.com"
try:
    author_list
    print("Author list already loaded.")
except NameError:
    try:
        author_list = json.load(open("data/author_list.json"))
        print("Author list loaded from file.")
    except FileNotFoundError:
        author_list = []
        print("Author list file not found. An empty list has been initialized.")

author_ids = {author['id'] for author in author_list}

nest_asyncio.apply()


async def fetch_author(session, url, author_ids, author_list):
    async with session.get(url) as response:
        author_data = await response.json()
        if author_data['id'] not in author_ids:
            author_list.append(author_data)
            author_ids.add(author_data['id'])


async def get_authors():
    url = f"{base_url}authors/random?mailto={email}"
    author_ids = {author['id'] for author in author_list}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(10):
            tasks.append(fetch_author(session, url, author_ids, author_list))
            # Adding a delay to respect the rate limit
            await asyncio.sleep(0.1)
        await asyncio.gather(*tasks)

i = 0
try:
    while len(author_list) < 100000:
        asyncio.run(get_authors())
        print(
            f"Iteration {i + 1} completed: {len(author_list)} authors collected.")
        if i % 100 == 0:
            print("Saving author list to file...")
            with open("data/author_list.json", "w") as outfile:
                json.dump(author_list, outfile, indent=4)
        i += 1
except KeyboardInterrupt:
    print("Interrupted by user. Saving author list to file...")
    with open("data/author_list.json", "w") as outfile:
        json.dump(author_list, outfile, indent=4)
    print("Author list saved. Exiting program.")
