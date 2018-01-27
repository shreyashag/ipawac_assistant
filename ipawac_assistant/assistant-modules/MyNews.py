# -*- coding: utf-8-*-
# https://newsapi.org/#documentation
import re
import requests
import json

WORDS = ["NEWS"]


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
    # speaker.clean_and_say(message)
    news_source = 'the-times-of-india'
    responseObject = requests.get(
        'https://newsapi.org/v1/articles?apiKey=61332d3cb3de480caf23c825bd090ec2' +
        '&source=' +
        news_source)
    responseData = responseObject.json()
    print(
        json.dumps(
            responseData,
            sort_keys=True,
            indent=2,
            separators=(
                ',',
                ': ')))


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'news', text, re.IGNORECASE))
