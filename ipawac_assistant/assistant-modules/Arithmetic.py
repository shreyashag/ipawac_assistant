# -*- coding: utf-8-*-
import re

WORDS = ["MATHS", "ARITHMETIC"]


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
    message = "Please tell me what you would like to calculate (two numbers, +,-,*,/"
    speaker.clean_and_say(message)
    arithmetic_question = mic.activeListen()

    # SPLICE THE SENTENCE INTO A LIST AND THEN SEARCH THE LIST

    if ("+" in arithmetic_question):
        #speaker.clean_and_say("Addition detected")
        addition_list = []
        addition_list.append(
            re.findall(
                "[-+]?\d+[\.]?\d*",
                arithmetic_question))
        arithmetic_sum = float(
            addition_list[0][0]) + float(addition_list[0][1])
        speaker.clean_and_say(" The sum is " + str(arithmetic_sum))
    elif ("MINUS" in arithmetic_question):
        #speaker.clean_and_say("Subtraction detected")
        addition_list = []
        addition_list.append(
            re.findall(
                "[-+]?\d+[\.]?\d*",
                arithmetic_question))
        arithmetic_difference = float(
            addition_list[0][0]) - float(addition_list[0][1])
        speaker.clean_and_say(
            " The difference is " +
            str(arithmetic_difference))
    elif ("INTO" in arithmetic_question):
        #speaker.clean_and_say("Multiplication module now")
        addition_list = []
        addition_list.append(
            re.findall(
                "[-+]?\d+[\.]?\d*",
                arithmetic_question))
        arithmetic_product = float(
            addition_list[0][0]) * float(addition_list[0][1])
        speaker.clean_and_say(" The product is " + str(arithmetic_product))
    elif ("DIVIDED" in arithmetic_question):
        #speaker.clean_and_say("Division module now")
        addition_list = []
        addition_list.append(
            re.findall(
                "[-+]?\d+[\.]?\d*",
                arithmetic_question))
        arithmetic_quotient = float(
            addition_list[0][0]) / float(addition_list[0][1])
        speaker.clean_and_say(" The quotient is " + str(arithmetic_quotient))
    else:
        speaker.clean_and_say("No arithmetic module selected")


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    if re.search(r'\bMATHS\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bARITHMETIC\b', text, re.IGNORECASE):
        return True
