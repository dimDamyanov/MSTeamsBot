import json
with open('team_names.json') as json_file:
    data = json.load(json_file)

for key in data.keys():
    print(key)
    data[key] = input()

with open('team_names.json', 'w') as json_file:
    json.dump(data, json_file)