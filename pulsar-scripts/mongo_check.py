from pymongo import MongoClient
import pandas as pd

mongo_client = MongoClient('localhost',27017)

collection = mongo_client.github['repository']
data = collection.find()

df = pd.json_normalize(data)
#print(df.iloc[0]["tests"])
#print(f'number -1 no commits = {df[df["no_commits"] == -1].shape}')
print(df.shape)
