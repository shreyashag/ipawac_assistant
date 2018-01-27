# -*- coding: utf-8-*-
import re


WORDS = ["CALL"]


def handle(text, mic, profile, linphone):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    try:
        if re.search(r'\bEnd call\b', text, re.IGNORECASE):
            linphone.end_call()
            speaker.clean_and_say("Alright, I have ended the call")
        if re.search('aman', text, re.IGNORECASE):
            speaker.clean_and_say("Calling Aman Salehjee!")
            linphone.create_call('amansalehjee')
        elif re.search('shreyash', text, re.IGNORECASE):
            speaker.clean_and_say("Calling shreyash!")
            linphone.create_call('shreyash23')
        elif re.search('nikhil', text, re.IGNORECASE):
            speaker.clean_and_say("Calling nikhil!")
            linphone.create_call('nikhil93')
    except KeyboardInterrupt:
        linphone.end_call()


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'call', text, re.IGNORECASE))
