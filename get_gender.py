import os
import sys
import regex as re
import requests
import json
import pandas as pd
from pprint import pprint
import pickle
from openai import OpenAI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

openalex_url = "https://api.openalex.org/"


def pickle_dump(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


author_list = []
for j in range(10):
    try:
        author_list.extend(pickle.load(
            open(f"data/author_list_{j}.pkl", 'rb')))
        logging.info(f"Author list {j} loaded from file.")
    except FileNotFoundError:
        sample = 10000
        per_page = 200
        while j < 10:
            new_author_list = []
            logging.info(f"{j}th sample")
            seed = 3142 + j
            i = 1
            while i <= sample / per_page:
                logging.info(f"Page {i}")
                response = requests.get(openalex_url + "authors",
                                        params={'sample': sample, 'seed': seed, 'per-page': per_page, 'page': i, 'api_key': os.getenv("OPENALEX_API_KEY")})
                data = response.json()
                if len(data['results']) == 0:
                    break
                new_author_list.extend(data['results'])
                i += 1
            filename = f"data/author_list_{j}.json"
            logging.info(
                f'Saving {len(new_author_list)} authors to {filename}')
            pickle_dump(new_author_list, f"data/author_list_{j}.pkl")
            j += 1

authors_df = pd.DataFrame(author_list)

authors_df['strip_display_name'] = authors_df['display_name'].str.replace(
    '\.\s?', ' ', regex=True)

# Filter the DataFrame
df = authors_df[~authors_df['strip_display_name'].str.match(r'^\b\w{1,2}\b ')]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_gender_prediction(input_string):
    response = client.responses.create(
        model='gpt-3.5-turbo',
        instructions='You are a helpful assistant that determines the most likely gender of a person with specified name: responding only with "Male", "Female", or "Unknown".',
        input=f"{input_string}."
    )
    logging.info(f"Response: {response}")
    # Extract the response text
    gender = response.output_text
    return gender


chunk_size = 1000
df['probable_gender'] = None

for start in range(0, len(df), chunk_size):
    end = start + chunk_size
    chunk = df.iloc[start:end]
    chunk['probable_gender'] = chunk['display_name'].apply(
        lambda x: get_gender_prediction(x))
    df.update(chunk)
    pickle_dump(df, f"data/gender_predictions_{start}_{end}.pkl")
    logging.info(f"Processed and saved chunk {start} to {end}")
