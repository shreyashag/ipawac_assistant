# -*- coding: utf-8-*-
import re
from client import brain
from client import conversation

WORDS = ["RELOAD", "MODULES"]


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
    conversation.Brain.modules = []
    conversation.Brain.modules = brain.Brain.get_modules()
    speaker.clean_and_say("Modules Reloaded!")


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bReload modules\b', text, re.IGNORECASE))
