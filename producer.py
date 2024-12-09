import pulsar
import pickle
import json
from pulsar.schema import *
import requests
from datetime import datetime, timedelta
import pandas as pd
from itertools import cycle
import os
# Create a pulsar client by supplying ip address and port
tokens = ["add tokens"]
client = pulsar.Client('pulsar://localhost:6650')

# Create a producer on the topic that consumer can subscribe to
N_CONSUMERS = int(os.environ["N_CONSUMERS"])
producers = []
for n in range(N_CONSUMERS):
    producers.append(client.create_producer(f'produce-{n}'))

def get_repositories_for_token(current_token, current_page, start_date, end_date):

    # Base URL for the GitHub API endpoint
    base_url = "https://api.github.com/search/repositories"

     # Parameters for the initial request
    params = {
        'q': 'created:{}..{}'.format(start_date, end_date),
        'page': current_page,
        'per_page': 100 #default results per page is 100, and that is also the maximum result per page
    }

    # Make a request to the GitHub API
    response = requests.get(base_url, 
                            params=params,
                            headers={
                                'Accept': 'application/vnd.github+json',
                                'Authorization': 'Bearer ' + current_token,
                                'X-GitHub-Api-Version': '2022-11-28'
                            })
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data["items"]
    else:
        # Print an error message if the request was not successful
        print("Error:", response.status_code)
        return []


def search_github_repositories():
    # Define the search parameters
    # Get last year's data
    days_of_year = 365
    today = datetime.now()
    start_date_one_year_ago = today.replace(year=today.year - 1) +timedelta(days=15)
    maximum_number_of_pages_per_token = 10 #as we can only get 1000 results per api call

    for day in range(5):
        #if today is 26-05-2024, then this would give data for 26-05-2023 for the first run, then 27-05-2023 the next run
        start_date = start_date_one_year_ago + timedelta(days=day)
        end_date = start_date + timedelta(days=1) #limit bottom to only get one days worth of data
        str_start_date = start_date.isoformat()
        str_end_date = end_date.isoformat()
        print("Date of data: ", str_start_date)
        token_nr = 0

        for page in range(10): # minus one as j is equal to pages and pages start with the first page
            token = tokens[token_nr]
            print("Current_page fetched: ", page+1)
            all_items = get_repositories_for_token(token, page+1, str_start_date, str_end_date)
            zip_list = zip(all_items,cycle(producers))
            print("Sending number repos: ",len(all_items))
            for repo,producer in zip_list:
                #print(repo)
                producer.send(json.dumps(repo).encode("utf-8"))
            token_nr += 1
            if token_nr > len(tokens)-1:
                token_nr = 0
    

# Example usage
repositories = search_github_repositories()
for producer in producers:
    producer.send(("exit").encode("utf-8"))
    
# Destroy pulsar client
client.close()
