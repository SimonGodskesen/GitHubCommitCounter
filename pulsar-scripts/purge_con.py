import pulsar
import json
import ast
import pandas as pd
import time
import re
import pickle
from pulsar.schema import *
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')
# Subscribe to a topic and subscription
consumers = []
for m in range(2):
    consumers.append(client.subscribe(f'produce-{m}', subscription_name=f'GitHub-sub-{m}'))

while True:
    msg = consumers[1].receive()
    consumers[1].acknowledge(msg)


client.close()
