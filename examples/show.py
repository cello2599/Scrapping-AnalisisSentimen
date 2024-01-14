import json

with open('coba_scrap.json', 'r') as file:
    info_data = json.load(file)

print(info_data['user']['uniqueId'])