import spacy
from pymongo import MongoClient
from spacy import displacy
limitQuery = 65
orderQuery = -1

nlp = spacy.load('/var/www/html/en_edit_web_lg')

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find().limit(limitQuery).sort([('_id',orderQuery)])

for event in allEvents:
	entities = []
	entitiesAllowed = ['ORG','GPE','LOC','PERSON','PRODUCT']
	doc = nlp(event['details'])
	
	for ent in doc.ents:
		if ent.label_ in entitiesAllowed:
			entities.append({ent.label_:ent.text})

	events.update({'_id':event['_id']},{"$set":{'entityAutomaticListLGAfterTraining':entities}},upsert=False)

