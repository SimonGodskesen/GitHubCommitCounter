#This file is used to clear mongoDB between runs,
# to make sure we have a cleansed database before re-runnint the script

from pymongo import MongoClient
import pandas as pd

mongo_client = MongoClient('localhost',27017)

try:
    mongo_client.drop_database('github')
except:
    pass
db = mongo_client.github
db.repository.create_index('name', unique=False)
