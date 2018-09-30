# -*- coding: utf-8 -*-
import scrapy
import pymongo
from scrapy import Selector
import time
from random import randint
from w3lib.html import remove_tags
from scrapy.conf import settings

class EventbriteComBrSpider(scrapy.Spider):
    name = 'eventbrite.com.br'
    allowed_domains = ['eventbrite.com']
    settings.overrides['DOWNLOAD_DELAY'] = 3

    start_urls = [
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=1',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=2'
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=3',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=4',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=5',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=6',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=7',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=8',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=9',
        'https://www.eventbrite.com/d/ca--san-francisco/science-and-tech--events/?page=10'
    ]

    # 1. Connect to MongoDB instance running on localhost
    client = pymongo.MongoClient()
    collection = client.eventbrite.eventbrite

    def parse(self, response):
        urlEvents = response.css('.search-event-card-wrapper aside a::attr(href)').extract()
        urlEventsList = []

        #Para seguir a politica de utilização, deixo o script dormindo num intervalo entre 30 e 50 segundos
        #time.sleep(3)
        #Percorro a lista de eventos existentes em cada uma das páginas e adiciono em um array
        for urlEvent in urlEvents:
            urlEventsList.append(urlEvent)

        #Percorro cada uma das urls e coleto os dados existentes
        for urlToAccessDataEvent in urlEventsList:
            #Para seguir a politica de utilização, deixo o script dormindo num intervalo entre 30 e 50 segundos
            #time.sleep(5)
            yield response.follow(urlToAccessDataEvent,self.parse_event_details)

        pass


    def parse_event_details(self, response):
        eventData   = {
            "title":None,
            "location":None,
            "details": None,
            "timeList":None
        }

        try:

            eventTitle = response.css('main .listing-hero-body meta::attr(content)').extract_first()
            eventLocation = response.css('main .listing-map-card-street-address::text').extract_first()
            eventTimeList = response.css('main .event-details:not(.hide-small) .event-details__data time p:not(.hide-small.hide-medium)::text').extract()
            eventDetails = ""

            eventDetails = remove_tags(response.css('main .read-more__toggle-view').extract_first())

            eventData["title"] = eventTitle
            eventData["location"]   = eventLocation.strip()
            eventData["timeList"]   = eventTimeList
            eventData["details"]    = eventDetails

            self.collection.insert_one(dict(eventData))

        except:
            print "Error................"
