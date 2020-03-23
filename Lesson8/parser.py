from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from datetime import date
import calendar

weather = []
year = 2014
while year < 2020:
    for month in range(1, 13):
        col_days = calendar.monthrange(year, month)[1]
        main_link = f'https://www.gismeteo.ru/diary/4862/{year}/{month}/'
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        res = requests.get(main_link, headers=headers)
        response = res.text
        root = html.fromstring(response)

        for i in range(1, col_days+1):
            t = root.xpath(f'//tr[{i}]//td[2]/text()')
            if len(t) == 1:
                t = t[0]
            else:
                continue
            weather_data = {}
            weather_data['year'] = year
            weather_data['month'] = month
            weather_data['day'] = i
            weather_data['temperature'] = t
            weather.append(weather_data)
    year = year + 1

client = MongoClient('localhost', 27017)
db = client['test']
for collection_name in db.list_collection_names():
    if collection_name == 'weather':
        collection = db['weather']
        collection.drop()

result = db.weather.insert_many(weather)