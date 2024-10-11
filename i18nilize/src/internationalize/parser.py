import json

# Function to parse json file, given its path
def parse_json_file(path):
    # open file
    with open(path, 'r') as file:
        data = json.load(file)
    return data