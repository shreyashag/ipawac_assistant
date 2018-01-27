# -*- coding: utf-8-*-
import datetime
import re
from assistant.plugins.utilities.app_utils import getTimezone

WORDS = ["TIME"]


def handle(text, mic, speaker, profile, visionProcess):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    time = now.strftime("%I:%M:%S %p")
    date = now.strftime("%b %d %Y")
    speaker.clean_and_say(
        "It is %s right now and the date is %s" %
        (time, date))


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btime\b', text, re.IGNORECASE))
