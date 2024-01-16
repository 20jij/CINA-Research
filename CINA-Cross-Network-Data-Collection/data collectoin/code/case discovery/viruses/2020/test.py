import json

# Replace 'your_file.json' with the path to your JSON file.
file_path = '/Users/jasonji/Desktop/CINA/code/case_discovery/viruses/2020/entire_network.json'

try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        if isinstance(data, dict):
            dict_length = len(data)
            print(f"The length of the dictionary is: {dict_length}")
        else:
            print("The JSON data does not represent a dictionary.")
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
