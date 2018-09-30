from pymongo import MongoClient

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
average = banco['eventbrite_average']
allEvents = events.find()

data	= {}
data['averageSM'] = 0.0
data['averageMD'] = 0.0
data['averageLG'] = 0.0
totalValid = 0

for event in allEvents:

	if event['entityManualList'] is not None:
		totalValid += 1
		data['averageSM'] += event['accuracySM']
		data['averageMD'] += event['accuracyMD']
		data['averageLG'] += event['accuracyLG']
		
data['averageSM'] = round((data['averageSM'] * 1.0) / totalValid,2)	
data['averageMD'] = round((data['averageMD'] * 1.0) / totalValid,2)
data['averageLG'] = round((data['averageLG'] * 1.0) / totalValid,2)

average.insert_one(dict(data))


