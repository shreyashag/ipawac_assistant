# -*- coding: utf-8-*-
import random
import re
import os
import signal
import psutil
from subprocess import check_output

WORDS = ["QUIT", "OFF", "EXIT"]


def kill_process(name):
    for rethinkDBprocessID in (
            map(int, check_output(["pidof", name]).split())):
        # print (rethinkDBprocessID)
        os.kill(int(rethinkDBprocessID), signal.SIGKILL)


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()


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
    messages = ["Ok quitting, Bye bye!",
                "See you soon!"]

    message = random.choice(messages)

    speaker.clean_and_say(message)
    assistantPid = os.getpid()
    kill_process("rethinkdb")
    kill_proc_tree(os.getpid())


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bturn off\b', text, re.IGNORECASE)) or \
        bool(re.search(r'\bquit\b', text, re.IGNORECASE)) or \
        bool(re.search(r'\bexit\b', text, re.IGNORECASE))
