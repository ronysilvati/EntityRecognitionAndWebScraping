from pymongo import MongoClient
limitQuery = 65
orderQuery = -1
collectionAverage = 'eventbrite_average'

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
average = banco[collectionAverage]
allEvents = events.find().limit(limitQuery).sort([('_id',orderQuery)])

data	= {}
data['averageSMAfterTraining'] = 0.0
data['averageMDAfterTraining'] = 0.0
data['averageLGAfterTraining'] = 0.0
totalValid = 0

for event in allEvents:

	if event['entityManualList'] is not None:
		totalValid += 1
		data['averageSMAfterTraining'] += event['accuracySMAfterTraining']
		data['averageMDAfterTraining'] += event['accuracyMDAfterTraining']
		data['averageLGAfterTraining'] += event['accuracyLGAfterTraining']
		
data['averageSMAfterTraining'] = round((data['averageSMAfterTraining'] * 1.0) / totalValid,2)	
data['averageMDAfterTraining'] = round((data['averageMDAfterTraining'] * 1.0) / totalValid,2)
data['averageLGAfterTraining'] = round((data['averageLGAfterTraining'] * 1.0) / totalValid,2)

average.insert_one(dict(data))


