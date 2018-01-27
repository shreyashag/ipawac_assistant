# -*- coding: utf-8-*-
import random
import re

# WORDS = ["OPEN", "CLOSE"]


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
    messages = ["Shreyash is a brilliant guy.",
                "Shreyash is my master. Who is yours?!"]

    message = random.choice(messages)
    if bool(re.search(r'\bCLOSE WINDOW\b', text, re.IGNORECASE)):
        webbrowser.close()
    if bool(re.search(r'GOOGLE', text, re.IGNORECASE)):
        webbrowser.get("http://www.google.com")
    elif bool(re.search(r'FACEBOOK', text, re.IGNORECASE)):
        webbrowser.get("http://www.facebook.com")
    elif bool(re.search(r'youtube', text, re.IGNORECASE)):
        webbrowser.get("http://www.youtube.com")

    # speaker.clean_and_say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bCLOSE WINDOW\b', text, re.IGNORECASE) or
                re.search(r'\bOPEN GOOGLE\b', text, re.IGNORECASE) or
                re.search(r'\bOPEN YOUTUBE\b', text, re.IGNORECASE) or
                re.search(r'\bOPEN FACEBOOK\b', text, re.IGNORECASE))
