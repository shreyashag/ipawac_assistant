# -*- coding: utf-8-*-
# from sys import maxint
import random

WORDS = []

PRIORITY = -(999)


def handle(text, mic, speaker, profile, visionProcess):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    messages = ["I'm sorry, could you repeat that?",
                "My apologies, could you try saying that again?",
                "Say that again?", "I beg your pardon?"]

    message = random.choice(messages)

    speaker.clean_and_say(message)


def isValid(text):
    return True
