import json
import os.path

def update_db(data, client):
	if os.path.isfile('../database.json'):
		with open('../database.json', 'r') as fp:
			database = json.load(fp)
	else:
		database = {}

	for clientKey in data.keys():
		if clientKey not in database:
			database[clientKey] = client
		else:
			if(database[clientKey] != client):
				data.pop(clientKey, None)

	with open('../database.json', 'w') as fp:
		json.dump(database, fp)

	return data