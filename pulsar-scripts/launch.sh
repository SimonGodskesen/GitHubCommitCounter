#!/bin/bash

#Set the environment variable
echo "Please enter number of consumers:"
read n
export N_CONSUMERS=$n >> ~/.bashrc
source ~/.bashrc
# Run the Python script
python3 compose-build.py
echo "Launching containers..."
# Run docker-compose up in detached mode
docker-compose up -d

#wait for container to launch properly
echo "Configuring containers..."
sleep 20
#pip install pulsar-client pandas
python3 producer.py
