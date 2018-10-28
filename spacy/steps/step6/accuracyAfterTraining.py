from pymongo import MongoClient
limitQuery = 65
orderQuery = -1

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find().limit(limitQuery).sort([('_id',orderQuery)])

for event in allEvents:
	accuracySM = 0
	accuracyMD = 0
	accuracyLG = 0

	if event['entityManualList'] is not None:
		accuracySM = round(((len(event['manualAndAutomaticEqualitiesSMAfterTraining']) * 1.0) / len(event['entityManualList'])),2)
		accuracyMD = round(((len(event['manualAndAutomaticEqualitiesMDAfterTraining']) * 1.0) / len(event['entityManualList'])),2)
		accuracyLG = round(((len(event['manualAndAutomaticEqualitiesLGAfterTraining']) * 1.0) / len(event['entityManualList'])),2)
		
	
	events.update({'_id':event['_id']},{"$set":{'accuracySMAfterTraining':accuracySM,'accuracyMDAfterTraining':accuracyMD,'accuracyLGAfterTraining':accuracyLG}},upsert=False)

