from pymongo import MongoClient

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find().limit(65).sort([('_id',-1)])

for event in allEvents:
	accuracySM = 0
	accuracyMD = 0
	accuracyLG = 0

	if event['entityManualList'] is not None:
		accuracySM = round(((len(event['manualAndAutomaticEqualitiesSM']) * 1.0) / len(event['entityManualList'])),2)
		accuracyMD = round(((len(event['manualAndAutomaticEqualitiesMD']) * 1.0) / len(event['entityManualList'])),2)
		accuracyLG = round(((len(event['manualAndAutomaticEqualitiesLG']) * 1.0) / len(event['entityManualList'])),2)
		
	
	events.update({'_id':event['_id']},{"$set":{'accuracySM':accuracySM,'accuracyMD':accuracyMD,'accuracyLG':accuracyLG}},upsert=False)

