# -*- coding: utf-8 -*-
import spacy
from pymongo import MongoClient
from spacy import displacy
from spacy.scorer import Scorer
from spacy.gold import GoldParse

import plac
import random
from pathlib import Path
import sys
reload(sys)
sys.setdefaultencoding('utf8')

nlp = spacy.load('en_core_web_sm')

cliente = MongoClient('localhost', 27017)
banco = cliente['eventbrite']
events = banco['eventbrite']
allEvents = events.find({'entityManualList': {'$ne': None}}).limit(1).sort([('_id',1)])
output_dir = "/var/www/html/en_edit_web_sm"

TRAIN_DATA = []


for event in allEvents:
	entities = []
	
	for entt in event['entityManualList']:
		entities.append((int(entt['start']),int(entt['end']),entt['type']))

	TRAIN_DATA.append((event['details'],entities))

scorer = Scorer()
TRAIN_DATA	= [
	("End summer with science: Immerse yourself in the natural world at the California Academy of Sciences’ 6th annual #TeenScienceNight, a teen takeover night at the museum. Bay Area youth (ages 13 - 18) are invited to come relax and explore the world of science at this free, fun-filled event. Watch science come to life on August 17th from 6:30pm - 9:00pm at #TeenScienceNight - planned for youth, by youth. Hosted and organized by the California Academy of Sciences Youth Programs.#TeenScienceNight Who: Teens (13-18 years old)What: Science, music, food, and programsWhere: The California Academy of Sciences in Gold Gate ParkWhen: August 17, 2018 from 6:30pm - 9:00pmHow: Register via EventBrite to secure your ticket. The event may fill up, so make sure to RSVP as soon as possible. Partners: Chabot Space &amp; Science Center, The Marine Mammal Center, de Young Museum, Contemporary Jewish Museum, The Mix @ SFPL, Teen TechSF, Walt Disney Family Museum, San Francisco Zoo &amp; Gardens, KQED,  SF Opera, Presidio Trust, Outward Bound California, Sf Department of the Environment, Horizons School of Technology, LocoBloco, &amp; the Center for Urban Education about Sustainable Agriculture. ",[(169,177,'LOC')])
]
for input_, annot in TRAIN_DATA:
	doc_gold_text = nlp.make_doc(unicode(input_))
	gold = GoldParse(doc_gold_text, entities=annot)
	pred_value = nlp(unicode(input_))
	scorer.score(pred_value, gold)
print '-----------------------------'
print scorer.scores

