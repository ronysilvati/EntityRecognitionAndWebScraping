import spacy
from pymongo import MongoClient
from spacy import displacy


import plac
import random
from pathlib import Path

nlp = spacy.load('en_core_web_md')

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find({'entityManualList': {'$ne': None}}).limit(56).sort([('_id',1)])
output_dir = "/var/www/html/en_edit_web_md"

TRAIN_DATA = []

for event in allEvents:
	entities = []
	
	for entt in event['entityManualList']:
		entities.append((int(entt['start']),int(entt['end']),entt['type']))

	TRAIN_DATA.append((event['details'],{'entities':entities}))

model = 'en_core_web_md'
nlp = spacy.load(model)
print("Model '%s' carregado" % model)
ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
	for ent in annotations.get('entities'):
		ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):
	optimizer = nlp.begin_training()
	for itn in range(100):
		random.shuffle(TRAIN_DATA)
		losses = {}

		for text, annotations in TRAIN_DATA:
			nlp.update(
				[text],
				[annotations],
				drop=0.5,
				sgd=optimizer,
				losses=losses
			)

	for text, _ in TRAIN_DATA:
        	doc = nlp(text)
        	print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
       		print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])


	# save model to output directory
    	if output_dir is not None:
        	output_dir = Path(output_dir)
        	if not output_dir.exists():
            		output_dir.mkdir()
        		nlp.to_disk(output_dir)
        		print("Saved model to", output_dir)

        	# test the saved model
        	print("Loading from", output_dir)
        	nlp2 = spacy.load(output_dir)
        	for text, _ in TRAIN_DATA:
            		doc = nlp2(text)
            		print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
           		#print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])




