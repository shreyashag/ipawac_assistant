# -*- coding: utf-8-*-
import re

# https://github.com/geekpradd/PyDictionary
from PyDictionary import PyDictionary

WORDS = ["DEFINE", "DEFINITION"]


def handle(text, mic, speaker, profile, visionProcess):

    lst = text.split()

    text = lst[len(lst) - 1]
    if(text):
        dictionary = PyDictionary()
        mean = dictionary.meaning(text)
        if not mean:
            speaker.clean_and_say(
                "I'm sorry I couldn't find the meaning of the word " + text)
            return

        word = (text)
        types = []
        meanings = []
        for keys in mean:
            types.append(keys)
            output = "{} is a {}".format(word, (keys))
            lst = mean[keys]
            meaning = ''

            def cap(s, l):
                return s if len(s) <= l else s[0:l - 3] + '...'
            for l in lst:
                meaning = meaning + l
            meanings.append(
                "{} which means {}".format(
                    output, cap(
                        meaning, 500)))

        if (len(types) > 1):
            speaker.clean_and_say(
                "Found more than one meaning, which one do you want to hear about?")

            count = 0
            type_output = ''
            for item in (types):
                count = count + 1
                type_output = type_output + "\n" + str(count) + ". " + item

            speaker.clean_and_say(type_output)
            answer = mic.activeListen()

            speaker.clean_and_say(meanings[int(answer) - 1])
        else:
            speaker.clean_and_say(meanings[0])


def isValid(text):
    return bool(re.search(r'\bdefine|definition\b', text, re.IGNORECASE))
