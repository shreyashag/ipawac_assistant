# -*- coding: utf-8-*-
import random
import re

WORDS = ["WHO", "IS", "SHREYASH"]


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

    speaker.clean_and_say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bwho is shreyash\b', text, re.IGNORECASE))
