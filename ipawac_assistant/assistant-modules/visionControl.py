# -*- coding: utf-8-*-
from __future__ import print_function
import re

WORDS = ["VISION"]


def handle(text, mic, speaker, profile, vision_dict):

    if re.search(r'\bshow vision\b', text, re.IGNORECASE):
        vision_dict['vision_output_enabled'] = 1
    if re.search(r'\bhide vision\b', text, re.IGNORECASE):
        vision_dict['vision_output_enabled'] = 0

    if re.search(r'\bstart face vision\b', text, re.IGNORECASE):
        vision_dict['face_detector'] = 1
    if re.search(r'\bstop face vision\b', text, re.IGNORECASE):
        vision_dict['face_detector'] = 0

    if re.search(r'\blearn vision\b', text, re.IGNORECASE):
        speaker.clean_and_say("What is the person's name?")
        face_name = mic.activeListen()
        speaker.clean_and_say(
            "Alright, capturing images, please ensure there is only one person in frame to train")
        vision_dict['face_name'] = face_name
        vision_dict['training_started'] = 1
        while vision_dict['training_captured'] <= 20:
            pass
        speaker.clean_and_say("Capturing images done, now training!")
        while vision_dict['training_started'] == 1:
            pass
        speaker.clean_and_say(
            "Training done, new model is available with learned face!")


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bvision\b', text, re.IGNORECASE))
