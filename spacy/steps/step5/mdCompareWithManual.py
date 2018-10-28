from pymongo import MongoClient

limitQuery = 65
orderQuery = -1

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find().limit(limitQuery).sort([('_id',orderQuery)])

for event in allEvents:
	entitiesWithEqualsValues = []
	entitiesAllowed = ['ORG','GPE','LOC','PERSON','PRODUCT']
	
	if event['entityManualList'] is not None:
		for manual in event['entityManualList']:
			addNew = False

			for automatic in event['entityAutomaticListMDAfterTraining']:
				for type in automatic:
					if ((manual['value'] == automatic[type].lower()) and (manual['type'] == type)):
						addNew = True
			
			if addNew == True:
				entitiesWithEqualsValues.append({manual['type']:manual['value']})


		events.update({'_id':event['_id']},{"$set":{'manualAndAutomaticEqualitiesMDAfterTraining':entitiesWithEqualsValues}},upsert=False)

