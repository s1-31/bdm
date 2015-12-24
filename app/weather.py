# -*- coding:UTF-8 -*-

import urllib
import urllib2
import json
import datetime

import voice

class Weather(object):
    """docstring for Weather"""
    def __init__(self, api_key='d58dc2d55e55bf67313b4b490cb99647',country='jp',location='Tokyo'):
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

    def get_string(self):
        weather = self.get_weather()

        # string = '今日の天気は、' + str(weather['weather']) + 'です。'

        string1 = str(weather['datetime']) + '現在' + 'の' + str(weather['city']) + 'の天気は、' + str(weather['weather']) + 'です。'

        string2 = '最高気温は' + str(weather['temp_max']) + '度、最低気温は' + str(weather['temp_min']) + '度です。'

        return string1 + string2

if __name__ == '__main__':
    # api_key = 'd58dc2d55e55bf67313b4b490cb99647'
    # country = 'jp'
    # location = 'Tokyo'

    print Weather().get_weather()
    text =  Weather().get_string()
    print text
    voice.VoiceText(text=text).speak()
