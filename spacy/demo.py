from pymongo import MongoClient

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
average = banco['eventbrite_average']
allEvents = events.find()

total = 0

for event in allEvents:

	if event['entityManualList'] is None:
		total += 1

print total

