import json

def to_json(data):
    with open('1.json', 'w') as file:
        file.write(json.dumps(data))


