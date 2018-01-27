# -*- coding: utf-8-*-
import re

WORDS = ["SLEEP"]


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
    speaker.clean_and_say(
        "Going to sleep, you may wake me up by saying time to wake up")
    profile['sleeping'] = True


def isValid(text):
    """
        Returns True if the input is go to sleep

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bgo to sleep\b', text, re.IGNORECASE))
