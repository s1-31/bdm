# -*- coding:UTF-8 -*-

import urllib
import urllib2
import json
import datetime

class Weather(object):
    """docstring for Weather"""
    def __init__(self, api_key, country, location):
        super(Weather, self).__init__()
        self.APIKEY = api_key
        self.country = country
        self.location = location

    def get_weather(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?q='+self.location+','+self.country+'&APPID='+self.APIKEY
        res = urllib2.urlopen(url)
        line = res.readline()
        data = json.loads(line)

        weather = {}
        weather['weather'] = data['weather'][0]['main']
        weather['detail'] = data['weather'][0]['description']
        weather['temp_max'] = data['main']['temp_max'] - 273.15
        weather['temp_min'] = data['main']['temp_min'] - 273.15
        weather['humidity'] = data['main']['humidity']
        weather['city'] = data['name']
        weather['time'] = data['dt']
        weather['datetime'] = datetime.datetime.fromtimestamp(data['dt'])
        return weather

if __name__ == '__main__':
    api_key = 'd58dc2d55e55bf67313b4b490cb99647'
    country = 'jp'
    location = 'Tokyo'
    print Weather(api_key=api_key, country=country, location=location).get_weather()
