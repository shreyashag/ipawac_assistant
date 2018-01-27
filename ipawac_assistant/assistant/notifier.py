# -*- coding: utf-8-*-
import queue
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import time
import threading


class Notifier(object):

    class Timer(threading.Thread):  # subclass Thread
        # make it possible to pass the time in seconds that we want the timer
        # to run
        def __init__(self, seconds):
            self.runTime = seconds  # set our runTime in seconds
            threading.Thread.__init__(self)  # call the Thread's constructor

        def run(self):  # define what we want our Timer thread to do
            time.sleep(self.runTime)  # have it sleep for runTime seconds
            print("Buzzzz!! Time's up!")

    class Alarm(threading.Thread):
        # make it possible to pass the time in seconds that we want the timer
        # to run
        def __init__(self, seconds):
            self.runTime = seconds  # set our runTime in seconds
            threading.Thread.__init__(self)  # call the Thread's constructor

        def run(self):  # define what we want our Timer thread to do
            time.sleep(self.runTime)  # have it sleep for runTime seconds
            print("Buzzzz!! Time's up!")

    class GoogleNotificationClient(object):
        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile, vision_dict):
        self._logger = logging.getLogger(__name__)
        self.q = queue.Queue()
        self.profile = profile
        self.vision_dict = vision_dict
        # self.credentials = gmail_controller.get_credentials();
        # self.http = self.credentials.authorize(httplib2.Http())

        # self.googleService = discovery.build('gmail', 'v1', http=self.http)
        self.notifiers = []

        # self.notifiers = [self.GoogleNotificationClient(self.handleEmailNotifications, None)]

        # if 'gmail_address' in profile and 'gmail_password' in profile:
        #     self.notifiers.append(self.NotificationClient(
        #         self.handleEmailNotifications, None))
        # else:
        #     self._logger.warning('gmail_address or gmail_password not set ' +
        #                          'in profile, Gmail notifier will not be used')

        sched = BackgroundScheduler(timezone="UTC", daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        # sched.add_job(self.clear_message, 'interval', seconds=40)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def clear_message(self):
        self.vision_dict['message'] = ''

    def handleEmailNotifications(self, lastDate):
        """Places new Gmail notifications in the Notifier's queue."""
        # Gmail.ListMessagesMatchingQuery(self.googleService,'me',60,'is:inbox is:unread')
        # Gmail.ListHistory(self.googleService)
        return lastDate

    def getNotification(self):
        """Returns a notification. Note that this function is consuming."""
        try:
            notif = self.q.get(block=False)
            return notif
        except queue.Empty:
            return None

    def getAllNotifications(self):
        """
            Return a list of notifications in chronological order.
            Note that this function is consuming, so consecutive calls
            will yield different results.
        """
        notifs = []

        notif = self.getNotification()
        while notif:
            notifs.append(notif)
            notif = self.getNotification()

        return notifs
