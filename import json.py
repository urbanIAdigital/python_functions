import json
import os

def get_object_ids(collection):
    return [item.get('objectid') for item in collection if 'objectid' in item]

# Load the JSON file
file_path = os.path.join(os.path.dirname(__file__), 'model_properties.json')
with open(file_path, 'r') as file:
    data = json.load(file)

# Assuming the collection is stored under a key named 'collection' in the JSON
if 'collection' in data and isinstance(data["data"]['collection'], list):
    collection = data["data"]['collection']
    object_ids = get_object_ids(collection)
    print("Object IDs:", object_ids)
else:
    print("The JSON file does not contain a 'collection' array.")
