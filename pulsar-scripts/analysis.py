
import re
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Connect to MongoDB
mongo_client = MongoClient('localhost', 27017)
db = mongo_client.github
collection = db.repository

# Load data from MongoDB
data = pd.DataFrame(list(collection.find()))
size = data.shape[0]
# Q1: Top 10 programming languages based on the number of projects developed
top_languages = data['language'].value_counts().head(10)

# Plotting Top 10 programming languages
plt.figure(figsize=(12, 8))
top_languages.plot(kind='bar', color='skyblue')
plt.title(f'Top 10 Programming Languages by Number of Projects\nNumber of repositories = {size}')
plt.xlabel('Programming Language')
plt.ylabel('Number of Projects')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('output/top_languages.png', dpi=300)

# Q2: Top 10 most frequently updated GitHub projects (most commits)
top_updated_projects = data.sort_values(by='no_commits', ascending=False).head(10)

# Plotting Top 10 most frequently updated GitHub projects
plt.figure(figsize=(12, 8))
plt.bar(top_updated_projects['name'], top_updated_projects['no_commits'], color='skyblue')
plt.title(f'Top 10 Most Frequently Updated GitHub Projects\nNumber of repositories = {size}')
plt.xlabel('Project Name')
plt.ylabel('Number of Commits')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('output/top_updated_projects.png', dpi=300)

# Q3: Top 10 programming languages that follow the test-driven development approach
# Check if there is a 'tests' variable inside the 'content_url'
test_driven = {}
#data = collection.find()

def func(contents):
    for file in contents:
        if bool(re.search("test",file["name"])):
            return True
    return False
data["has_tests"] = data["tests"].map(func)

for x in data.iterrows():
    if x[1]["has_tests"]:
        if x[1]['language'] not in test_driven:
            test_driven[f"{x[1]['language']}"] = 1
        else:
            test_driven[f"{x[1]['language']}"] += 1

sorted_list = sorted(test_driven.items(), key = lambda x:x[1], reverse = True)

m= 10
plt.figure(figsize=(12, 8))
plt.bar([e[0] for e in sorted_list[:m]],[e[1] for e in sorted_list[:m]],color='skyblue')
plt.title(f'Top 10 Most Languages with unit testing\nNumber of repositories = {size}')
plt.xlabel('Language')
plt.ylabel('Number of Repositories')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('output/top_languages_tests.png', dpi=300)

print("#Test Driven\tLanguage")
print("------------------------")
#for (a,b) in sorted_list[:list_length]:
#    print(f"{b}\t\t{a}")


# Save the plot as an image
#plt.savefig('output/top_test_driven_languages.png', bbox_inches='tight')

# Q4: Top 10 programming languages that follow test-driven development and DevOps approach
data['cicd.workflows'] = data['cicd.workflows'].apply(lambda x: x if isinstance(x, list) else [])
data['has_cicd'] = data['cicd.workflows'].apply(lambda x: len(x) > 0)
devops_languages = data[data['has_tests'] & data['has_cicd']]['language'].value_counts().head(10)

# Plotting Top 10 programming languages that follow test-driven development and DevOps approach
plt.figure(figsize=(12, 8))
devops_languages.plot(kind='bar', color='skyblue')
plt.title(f'Top 10 Programming Languages with CI/CD\nNumber of repositories = {size}')
plt.xlabel('Programming Language')
plt.ylabel('Number of Projects')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('output/devops_languages.png', dpi=300)

# Printing results to stdout
print("Top 10 Programming Languages by Number of Projects:")
print(top_languages)

print("\nTop 10 Most Frequently Updated GitHub Projects:")
print(top_updated_projects[['name', 'no_commits']])

#print("\nTop 10 Programming Languages with Unit Tests:")
#print(test_driven_languages)

print("\nTop 10 Programming Languages with Unit Tests and CI/CD:")
print(devops_languages)
