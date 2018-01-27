# -*- coding: utf-8-*-
import re

WORDS = ["BIRTHDAY"]


def handle(text, mic, speaker, profile, visionProcess):
    speaker.clean_and_say(
        "Getting the list of people who have birthdays today")
    # contains names
    birthday_list = r.today_birthday_list()

    for birthday_name in birthday_list:
        speaker.clean_and_say("{} has birthday today".format(birthday_name))


def isValid(text):
    """
        Returns True if the input is related to birthdays.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'birthday', text, re.IGNORECASE))
