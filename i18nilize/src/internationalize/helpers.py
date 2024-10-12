import json

def get_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Input: 
#   - file_path: path of json file
# Output: Token in json file
def get_token(file_path):
    data = get_json(file_path)
    token = data["Token"]
    return token