from lxml import html
import requests
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
import json

main_link = 'https://www.gismeteo.ru/diary/4862/2019/2/'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
response = requests.get(main_link, headers=headers).text
root = html.fromstring(response)
weather = []
for i in range(28):
    t = root.xpath(f'//tr[{i+1}]//td[2]/text()')[0]
    weather_data = {}
    weather_data['day'] = i+1
    weather_data['temperature'] = t
    weather.append(weather_data)

client = MongoClient('localhost', 27017)
db = client['test']
for collection_name in db.list_collection_names():
    if collection_name == 'weather':
        collection = db['weather']
        collection.drop()

result = db.weather.insert_many(weather)
pprint(result.inserted_ids)