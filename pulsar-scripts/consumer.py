import pulsar
import json
import ast
import pandas as pd
from pymongo import MongoClient
import re
from pymongo.errors import DuplicateKeyError
import argparse
import requests
import pickle
from pulsar.schema import *

#Our tokens
tokens = ["add tokens"]
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')

# Subscribe to a topic and subscription
parser = argparse.ArgumentParser(description='Consumer number')
parser.add_argument('-m', '--value_m', type=int, default=0, help='m = consumer number')
args = parser.parse_args()
m = args.value_m

#Connect to MongoDB
mongo_client = MongoClient('localhost',27017)
db = mongo_client.github

#Authorize the tokens, and append the authorization in the header_list
header_list = []
for token in tokens:
    header_list.append({"Authorization":f"token {token}"})

#Subscribe consumer to a specific producer
consumer = client.subscribe(f'produce-{m}', subscription_name=f'GitHub-sub-{m}')

data = pd.DataFrame()

token_nr = 0
while True:
    header = header_list[token_nr] #specify the current token being used
    msg = consumer.receive() #receive message for consumer
    decoded_msg = msg.data().decode("utf-8") 
    if decoded_msg == "exit":
        consumer.acknowledge(msg)
        if not data.empty:
            db.repository.insert_many(data.to_dict('records'))
        break
    
    #If the message isnt exit, then fetch the specific urls from the repo to fetch additional data
    repo_json = json.loads(decoded_msg)
    commit_url = repo_json["url"]+"/commits"
    content_url = repo_json["url"]+"/contents"
    workflow_url = repo_json["url"]+"/actions/workflows"


    #find number of commits - fetch additional JSON data about the commits in repo
    commit_response = requests.get(f'{commit_url}?&per_page=1&page=1',headers=header) #fetch the first commit, on the first page
    commit_data = commit_response.json()
    if commit_response.status_code == 200: #if the first commit was fetched successfully, find all other commits
        no_com = int(re.findall(r".+&page=(\d+)",commit_response.links["last"]["url"])[0])
    else:
        continue
    repo_json["no_commits"] = no_com

    #find filenames
    content_response = requests.get(f'{content_url}',headers=header)
    content_data = content_response.json()
    if content_response.status_code == 200:
        repo_json["tests"] = content_data
    else: 
        continue
    
    #find workflows
    wf_response = requests.get(f'{workflow_url}',headers=header)
    wf_data = wf_response.json()
    if wf_response.status_code == 200:
        repo_json["cicd"] = wf_data
    else: 
        continue

    repo_df = pd.json_normalize(repo_json)

    try:
        if not data.empty: #if the dataframe is not empty, add our new data to it
            data = pd.concat([data,repo_df])
        elif data.empty:
            data = repo_df #otherwise, replace the empty dataframe with our new data
        consumer.acknowledge(msg) 
    except:
        print("Repo failed to be added")
        consumer.negative_acknowledge(msg)
    
    token_nr += 1 #increment token_nr for next run in the while-loop
    
    if token_nr > len(tokens) - 1: #Reset the token_nr if it is beyond our number of tokens
        token_nr = 0

    if data.shape[0] == 20: #Connect to mongoDB for every 20th repository to be added, arbitraty number
        db.repository.insert_many(data.to_dict('records')) #adds data
        data = pd.DataFrame() #resets df


client.close()
