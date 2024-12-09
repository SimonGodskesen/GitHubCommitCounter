import argparse
import os
print(f"{int(os.environ['N_CONSUMERS'])} consumers")
s = """                                       
version: '3'
services:"""

for n in range(int(os.environ["N_CONSUMERS"])):
    s += """
  consumer"""+str(n)+""":
    image: apachepulsar/pulsar:2.7.0
    volumes:
      - ./consumer.py:/consumer.py  # Mount the test.py script into the container
    environment:
      - N_CONSUMERS=${N_CONSUMERS}
    command: bash -c "pip install pandas pymongo && python3 /consumer.py -m """+str(n)+""""
    network_mode: "host"
    """


with open("docker-compose.yml","w") as file:
    file.write(s)
