#!/bin/bash

sudo apt -y update
sudo apt -y upgrade
sudo apt install -y python3-pip docker.io docker-compose
sudo python3 -m pip install pandas pymongo pulsar-client
sudo docker run -p 27017:27017 -d mongodb/mongodb-community-server:latest
sudo docker run -d -p 6650:6650 -p 8080:8080 \
--mount source=pulsardata,target=/pulsar/data \
--mount source=pulsarconf,target=/pulsar/conf \
apachepulsar/pulsar:2.7.0 bin/pulsar standalone

sudo python3 clear_mongodb.py

echo "Successfully launched Pulsar and MongoDB"
