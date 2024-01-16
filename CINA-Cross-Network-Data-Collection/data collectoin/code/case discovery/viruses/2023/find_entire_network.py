# this code finds the entire network that contains the target (CVE) github repos.

import re
import json


input_file = "/Users/jasonji/Desktop/CINA/code/case_discovery/viruses/2023/target_repo_2023.txt"

github_urls =set()

with open(input_file, 'r') as input_file:
    for line in input_file:
        url = line.strip()
        if re.match(r'^https?://github\.com/', url):
            github_urls.add(url)


json_file_path = "/Users/jasonji/Desktop/CINA/code/case_discovery/viruses/2023/nvdcve-1.1-2023.json"
with open(json_file_path, 'r') as json_file:
    cve = json.load(json_file)
   
records = {}

# First find the CVE repo description
# Iterate through CVE_Items
for item in cve.get("CVE_Items", []):
    references = item.get("cve", {}).get("references", {}).get("reference_data", [])
    for reference in references:
        url = reference.get("url", "")
        if url in github_urls:
            description_data = item.get("cve", {}).get("description", {}).get("description_data", [])
            for description in description_data:
                value = description.get("value", "")
                if url not in records:
                    records[url] = {
                        "CVE Description" : []
                    }
                records[url]["CVE Description"].append(value)

# print(records)

# Then find corresponding StackOverflow Networks
# First find the edges/sid
with open('/Users/jasonji/Desktop/CINA/code/dependency_data_d1.txt') as f:
    lines = f.readlines()
    parent_repo = ''
    parent_id = 0
    for line in lines:
        line = line.strip()
        if line=='\n' or len(line)==0:
            continue
        splits = line.split(' ')

        if len(splits)==2:
            repo = splits[0][:-1]
            sid =  splits[1]
            # double check 
            match = re.findall('https://github\.com/[^"].+', repo)
            if len(match)==0:
                continue
            if repo in github_urls:
                if "Edges" not in records[repo]:
                    records[repo]["Edges"] = []
                edge = {
                    "SID": sid
                }
                records[repo]["Edges"].append(edge)

            parent_repo = repo
            parent_id = sid
            
        elif len(splits)==3:
            package = splits[1][:-1]
            repo = splits[2]
            # double check 
            match = re.findall('https://github\.com/[^"].+', repo)
            if len(match)==0:
                continue
            if repo in github_urls:
                if "Edges" not in records[repo]:
                    records[repo]["Edges"] = []
                edge = {
                    "ParentSID": parent_id,
                    "ParentRepo": parent_repo
                }
                records[repo]["Edges"].append(edge)

# Find the stackoverflow post data associated with the SID

# Create a dictionary to map Ids to Stack Overflow posts
file_path = "/Users/jasonji/Desktop/CINA/data/StackOverflow/complete_linked_posts.json"
with open(file_path, "r") as json_file:
    stackoverflow_post = json.load(json_file)

stackoverflow_id_to_post = {post["Id"]: post for post in stackoverflow_post}

# print(stackoverflow_id_to_post)

for entry in records.values():
    edges = entry.get("Edges", [])
    for edge in edges:
        sid = edge.get("SID") or edge.get("ParentSID")
        if sid in stackoverflow_id_to_post:
            stackoverflow_post = stackoverflow_id_to_post[sid]
            edge["StackOverflow_Post"] = stackoverflow_post


output_filename = "entire_network.json"

# Write the dictionary to the JSON file
with open(output_filename, "w") as json_file:
    json.dump(records, json_file, indent=4)


