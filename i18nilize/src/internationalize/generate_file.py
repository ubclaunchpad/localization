import json
from src.internationalize.helpers import create_json

# Input: None (for now)
# Output: None, but creates a local JSON file containing translations
def generate_file():
    file_content = {
        "Token": "85124f79-0829-4b80-8b5c-d52700d86e46",
        "translations" : [{
				"language": "French",
				"hello": "bonjour",
				"No": "Non",
				"Why": "pourquoi",
			},
			{
				"language": "Spanish",
				"hello": "Hola",
			},
		]
    }

    # transforms the dictionary object above into a JSON object
    json_object = json.dumps(file_content, indent=4)
    create_json(json_object)
