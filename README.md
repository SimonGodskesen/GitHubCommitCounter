## GitHub Commit Counter

This project uses the GitHub API to extract information about the most popular languages on GitHub.

By default, an API request of a repo doesn't include any information about the number of commits, workflows and filenames. They need to be extracted separately from a new API request.

This code analyses fetches repos, and makes additional API requests for each repo to obtain the following data, and why;

Language - Finds the most popular languages on github

Commits - Used to find most frequently updated repos

Filenames - Used to determine whether it uses a test-driven dev approach

Workflows - Used to determin whether it uses DevOps

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


About:
Coded by Simon Godskesen, except for get_repositories_for_token, and search_github_repositories functions in producer.py.
