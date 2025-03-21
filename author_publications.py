import asyncio
import aiohttp
import json
import os


author_list_path = "/Users/annamikulich/Desktop/p3/author_list.json"
output_path = "/Users/annamikulich/Desktop/p3/author_publications.json"


try:
    with open(author_list_path, "r") as file:
        author_list = json.load(file)
    print("Author list loaded from file.")
except FileNotFoundError:
    print(f"Author list file not found at {author_list_path}")
    author_list = []


async def fetch_publications(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("results", [])  
        else:
            print(f"Error fetching {url}: {response.status}")
            return []


async def get_author_publications():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for author in author_list:
            works_url = author.get("works_api_url")
            if works_url:
                print(f"Fetching: {works_url}") 
                tasks.append(fetch_publications(session, works_url))
            await asyncio.sleep(0.1)  

        publications = await asyncio.gather(*tasks)
        publications = [pub for sublist in publications for pub in sublist]  
        print(f"Total publications fetched: {len(publications)}")

        if publications:
            with open(output_path, "w") as outfile:
                json.dump(publications, outfile, indent=4)
            print(f"Publications saved to {output_path}")
        else:
            print("No publications were fetched.")


if __name__ == "__main__":
    asyncio.run(get_author_publications())
