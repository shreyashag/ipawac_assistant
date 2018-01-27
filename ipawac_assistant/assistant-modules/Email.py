# -*- coding: utf-8-*-
import re
import httplib2

from apiclient import discovery

from client.plugins import gmail_controller
from client.plugins import rethinkdb_connector

WORDS = ["EMAIL"]


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
    credentials = gmail_controller.get_credentials()
    http = credentials.authorize(httplib2.Http())
    googleService = discovery.build('gmail', 'v1', http=http)

    if re.search(
        'configure',
        text,
        re.IGNORECASE) or re.search(
        'set up email',
        text,
            re.IGNORECASE):
        speaker.clean_and_say(
            "Would you like to sign in using this device or another ( if on the Pi)?")
        speaker.clean_and_say(
            "Ok, setting up gmail, please sign in with your google account.")
        credentials = gmail_controller.get_credentials()

    if re.search('send', text, re.IGNORECASE):
        if re.search('(?<=TO)(.*)', text, re.IGNORECASE):
            print("Found word TO.. that means reciever is specified")

            temp = re.search("TO (\w+)", text, re.IGNORECASE)
            reciever_name = str(temp.group(1))

            # start search for first name
            #temp2 = re.search(reciever_name+" (\w+)", text)
            #reciever_name_complete = reciever_name + " " + str(temp2.group(1))

            # fetch email id from Database
            reciever_emailID = rethinkdb_connector.get_contact_value(
                reciever_name)

            if reciever_emailID == -1:
                speaker.clean_and_say(
                    "Email id not found in database, please specify it manually.")
                reciever_emailID = mic.activeListen()

            speaker.clean_and_say(
                'The email id is {}'.format(reciever_emailID))
            speaker.clean_and_say("Ok what is the SUBJECT?")
            subject = mic.activeListen()
            speaker.clean_and_say("Ok what do you want to send?")
            subject_body = mic.activeListen()
            # speaker.clean_and_say("Do you want to attach something with it (a selfie)?")
            # answer=mic.activeListen()
            # if re.search(r"\bYES",answer, re.IGNORECASE):
            #     speaker.clean_and_say("3")
            #     time.sleep(1)
            #     speaker.clean_and_say("2")
            #     time.sleep(1)
            #     speaker.clean_and_say("1")
            #     speaker.clean_and_say("SAY CHEESE!")
            #     #clickPhoto and get file_path
            # message = gmail_controller.create_message_with_attachment('shreyash.agarwal93@gmail.com', reciever_emailID, subject, subject_body, file):
            # else:

            message = gmail_controller.create_message(
                googleService, reciever_emailID, subject, subject_body)
            gmail_controller.send_message(googleService, 'me', message)
            speaker.clean_and_say("Message sent successfully!")

    if re.search('show', text) or re.search(r'do i have', text, re.IGNORECASE):
        if re.search('(?<=show)(.*)', text, re.IGNORECASE):
            print("Found word show.. need to fetch emails")

            # if re.search('show', text):
            #     temp = re.search("LAST (\w+)", text, re.IGNORECASE)
            #     numberOfEmails= str(temp.group(1))

            # if re.search('recent', text):
            #     temp = re.search("recent (\w+)", text, re.IGNORECASE)
            #     numberOfEmails= str(temp.group(1))
        speaker.clean_and_say("Showing last 5 unread emails")
        gmail_controller.ListMessagesMatchingQuery(
            googleService, 'me', 5, 'is:inbox is:unread')

        # gmail_controller.getEmails(numberOfEmails)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(
        re.search(
            r'email',
            text,
            re.IGNORECASE)) or bool(
        re.search(
            r'emails',
            text,
            re.IGNORECASE))
