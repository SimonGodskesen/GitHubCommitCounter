# DE2project

## How to start the project
In a new VM, run: setup.sh

Then: sudo -E ./launch.sh

## Explanation of files in GitHub

setup.sh initializes the VM for pulsar. Launches MongoDB, Pulsar, and installs packages.

launch.sh launches the containers and producers and restores the results in MongoDB. Run it using "sudo -E ./launch.sh"

clear_mongodb.py clears the MongoDB database.

compose-build.py creates the docker-compose.yml file. --scale (in docker) cannot replace this since the code enumerates the consumers.

purge_con.py purges all awaiting messages in a topic, mostly used for debugging and testing.

mongo_check.py prints value counts for number of commits, and size of database. Used for debugging and quickly checking 


consumer.py is the consumer(s). Stores result in MongoDB

producer.py is the producer. Fetches 10 pages, 100 per page, for 2 days = 2000 repo. (can be changed).

How to use:
Run setup.sh ONLY ONCE PER VM.
Run "sudo -E ./launch.sh" and select the number of consumers.
Run mongo_check.py to quickly check result.

Consumers might take a while and slowly build up the database. Use "sudo bash" then "docker ps" to see if consumers are still running.
