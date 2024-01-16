import json
import re

def extract_github_urls(data):
    github_urls = set()

    for item in data["CVE_Items"]:
        if "references" in item["cve"]:
            reference_data = item["cve"]["references"]["reference_data"]
            for reference in reference_data:
                url = reference["url"]
                if re.match(r'^https?://github\.com/', url):
                    github_urls.add(url)

    return github_urls

# Replace 'your_file.json' with the actual JSON file path
json_file_path = '/Users/jasonji/Desktop/CINA/code/case_discovery/viruses/nvdcve-1.1-2023.json'
output_file_path = '2023_github_urls.txt'

try:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        github_urls = extract_github_urls(data)

        if github_urls:
            with open(output_file_path, 'w') as output_file:
                for url in github_urls:
                    output_file.write(url + '\n')
        else:
            print("No GitHub Repository URLs found in the JSON file.")
except FileNotFoundError:
    print(f"File '{json_file_path}' not found.")
except json.JSONDecodeError:
    print(f"Error decoding JSON from '{json_file_path}'. Please ensure the file is in valid JSON format.")
except Exception as e:
    print(f"An error occurred: {e}")
