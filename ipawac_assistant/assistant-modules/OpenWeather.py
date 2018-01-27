# -*- coding: utf-8-*-
import re
import requests
import os
from client.plugins.utilities import jasperpath

WORDS = ["WEATHER"]


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def handle(text, mic, speaker, profile, visionProcess):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    #message = "Hold on, checking the weather for you..."
    # mic.say(message)

    location_name = "Bangalore"

    if re.search('(?<=TODAY)(.*)', text):
        weather_for = 'today'
    elif re.search('(?<=TOMORROW)(.*)', text):
        weather_for = 'tomorrow'
    elif re.search('(?<=THIS WEEK)(.*)', text):
        weather_for = 'this_week'
    elif re.search('(?<=NEXT WEEK)(.*)', text):
        weather_for = 'next_week'
    else:
        weather_for = 'today'

    if re.search('(?<=IN)(.*)', text, re.IGNORECASE):
        print("Found word in.. that means location is specified")
        location_temp = re.search("IN (\w+)", text, re.IGNORECASE)
        location_name = str(location_temp.group(1))
        name_start = ['NEW', 'SAN', 'ABU', 'PORT', 'KUALA', 'LOS']
        if location_name.upper() in name_start:
            print("Complex city name")
            location_temp2 = re.search(location_name + " (\w+)", text)
            location_name = location_name + " " + str(location_temp2.group(1))

    openWeatherCurrentUrl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
        location_name + '&units=metric&appid=4f95de0f661f4bb718a10067a7f27b60'
    openWeatherForeCastUrl = "api.openweathermap.org/data/2.5/forecast?q=" + \
        location_name + '&units=metric'

    responseObject = requests.get(openWeatherCurrentUrl)
    responseData = responseObject.json()

    temp_now = responseData['main']['temp']
    humidity = responseData['main']['humidity']
    description_short = responseData['weather'][0]['main']

    """
    sunset = responseData['sys']['sunset']
    sunrise = responseData['sys']['sunrise']
    temp_max = responseData['main']['temp_max']
    temp_min = responseData['main']['temp_min']
    temp_now = responseData['main']['temp']
    humidity = responseData['main']['humidity']
    description_short = responseData['weather'][0]['main']
    description_long = responseData['weather'][0]['description']
    print temp_max
    print temp_min
    print temp_now
    """

    iconCode = responseData['weather'][0]['icon']
    iconURL = 'http://openweathermap.org/img/w/' + iconCode + '.png'
    icon_path = jasperpath.WEATHER_ICONS + "/" + iconCode + '.png'

    if not os.path.isfile(icon_path):
        resp = requests.get(iconURL)
        if resp.status_code == 200:
            with open(icon_path, 'wb') as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)

    weather_message = "It is currently " + str(temp_now) + " degrees with " + str(
        humidity) + " percent humidity. The weather type is " + description_short
    # Need to modify message according to weather_for

    visionProcess['image_path'] = icon_path
    # visionProcess['message']=weather_message
    # visionProcess['message_timeout']=int(5)
    speaker.clean_and_say(weather_message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bWhat is the weather', text, re.IGNORECASE)
                or re.search(r'\bWhat\'s the weather', text, re.IGNORECASE)
                or re.search(r'\bHow\'s the weather', text, re.IGNORECASE)
                or re.search(r'\bHow is the weather', text, re.IGNORECASE))
