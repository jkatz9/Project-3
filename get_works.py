import requests
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

base_url = "https://api.openalex.org/"
email = os.getenv("EMAIL")
alex_key = os.getenv("OPENALEX_API_KEY")
oai_key = os.getenv("OPENAI_API_KEY")

# Specify drop columns
dropcolumns = [
    'orcid', 'display_name_alternatives', 'relevance_score', 'summary_stats', 'ids',
    'affiliations', 'last_known_institutions', 'topics', 'topic_share', 'updated_date', 'created_date'
]

# Generator function to read the JSONL file line-by-line


def read_jsonl_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield json.loads(line)

# Function to fetch data from the API


def fetch(url, params=None):
    logging.info(f"Fetching data from {url} with params {params}")
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

# Main function to process authors and fetch works


def main():
    authors_generator = read_jsonl_file('data/authors.jsonl')
    for author in authors_generator:
        works_api_url = author.get('works_api_url')
        if works_api_url:
            try:
                # Fetch works data
                result = fetch(works_api_url, params={
                               'mailto': email, 'api_key': alex_key})
                # Append results to works.jsonl
                with open('works.jsonl', 'a') as f:
                    for work in result.get('results', []):
                        f.write(json.dumps(work) + '\n')
                logging.info(
                    f"Successfully fetched and wrote data for {works_api_url}")
            except Exception as e:
                logging.error(f"Error fetching data for {works_api_url}: {e}")


# Run the main function
if __name__ == "__main__":
    main()
