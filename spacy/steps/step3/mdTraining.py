# -*- coding: utf-8 -*-
import spacy
from pymongo import MongoClient
from spacy import displacy
from spacy.scorer import Scorer
from spacy.gold import GoldParse
from tqdm import tqdm

import plac
import random
from pathlib import Path
import sys
reload(sys)
sys.setdefaultencoding('utf8')

nlp = spacy.load('en_core_web_md')

limitQuery = 66
orderQuery = 1 #1 = ASC, -1 = DESC
output_dir = "/var/www/html/en_edit_web_md"

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find({'entityManualList': {'$ne': None}}).limit(limitQuery).sort([('_id',orderQuery)])


TRAIN_DATA = []


for event in allEvents:
	entities = []
	
	for entt in event['entityManualList']:
		entities.append((int(entt['start']),int(entt['end']),entt['type']))

	TRAIN_DATA.append((event['details'],{"entities":entities}))

if 'ner' not in nlp.pipe_names:
	ner = nlp.create_pipe('ner')
	nlp.add_pipe(ner, last=True)
else:
	ner = nlp.get_pipe('ner')
	
for _, annotations in TRAIN_DATA:
	for ent in annotations.get('entities'):
		ner.add_label(ent[2])
		
	
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):
	optimizer = nlp.begin_training();
	
	for itn in range(50):
		random.shuffle(TRAIN_DATA)
		losses = {}
		
		for text, annotations in tqdm(TRAIN_DATA):
			nlp.update(
				[text],
				[annotations],
				drop=0.5,
				sgd=optimizer,
				losses=losses)
		
		print losses

nlp.to_disk(output_dir)
print("Saved")
