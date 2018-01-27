# -*- coding: utf-8-*-
import random
import re
import requests

WORDS = ["JOKE"]


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
    messages = ['Ok, I can be funny', 'Spreading some laughter with you now']
    message = random.choice(messages)
    speaker.clean_and_say(message)
    #webknoxJokeUrl = "http://webknox.com/api/jokes/random?apiKey=begaiafahcqgeehiaiuuwkrrnqkfnnh"
    #joke_resonse = requests.get(webknoxJokeUrl)

    jokeUrl2 = 'http://api.icndb.com/jokes/random'
    joke_resonse = requests.get(jokeUrl2)
    joke_content = joke_resonse.json()

    #webknoxJokeMessage = "Here is a " + str(joke_content['category']) +' joke . ' + str(joke_content['joke'])
    jokeMessage = str(joke_content['value']['joke'])

    speaker.clean_and_say(jokeMessage)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btell me a joke\b', text, re.IGNORECASE)
                or re.search(r'\bhow about a joke\b', text, re.IGNORECASE))
