# -*- coding: utf-8-*-
import re
import threading
import time

from client.plugins.utilities import jasperpath

WORDS = ["TIMER"]


class Timer(threading.Thread):  # subclass Thread
    # make it possible to pass the time in seconds that we want the timer to
    # run
    def __init__(self, seconds, speaker):
        self.runTime = seconds  # set our runTime in seconds
        threading.Thread.__init__(self)  # call the Thread's constructor
        self.speaker = speaker

    def run(self):  # define what we want our Timer thread to do
        time.sleep(self.runTime)  # have it sleep for runTime seconds
        self.speaker.clean_and_say("Timer is up!")
        self.speaker.play_wav_file(jasperpath.data('audio', 'timer.wav'))

# def handle(text, mic, speaker, profile, visionProcess, notifier):


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
    if re.search('(?<=for)(.*)', text, re.IGNORECASE):
        temp = re.search("for (\w+)", text, re.IGNORECASE)
        timer_duration = str(temp.group(1))

    if re.search(r'\bminutes\b', text, re.IGNORECASE):
        timer_duration = int(timer_duration) * 60

    timer = Timer(int(timer_duration), speaker)
    timer.start()
    speaker.clean_and_say("Timer set!")


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'set a timer for', text, re.IGNORECASE))
