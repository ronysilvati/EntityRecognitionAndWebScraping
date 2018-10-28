import spacy
from pymongo import MongoClient
from spacy import displacy

nlp = spacy.load('en_core_web_lg')

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find().limit(65).sort([('_id',-1)])

for event in allEvents:
	entities = []
	entitiesAllowed = ['ORG','GPE','LOC','PERSON','PRODUCT']
	doc = nlp(event['details'])
	
	for ent in doc.ents:
		if ent.label_ in entitiesAllowed:
			entities.append({ent.label_:ent.text})

	events.update({'_id':event['_id']},{"$set":{'entityAutomaticListLG':entities}},upsert=False)

