# -*- coding: utf-8-*-
import logging
import signal
import platform
import time
import multiprocessing
import os

from assistant.plugins.utilities import paths
from assistant.notifier import Notifier
from assistant.brain import Brain


from vision.camera_loop import camera_loop
from vision.gray_resizing_loop import gray_resizing_loop
from vision.face_detector_loop import face_detector_loop
from vision.face_learner_loop import face_learner_loop
from vision.face_recognizer_loop import face_recognizer_loop
from vision.jasper_vision_loop import jasper_vision_loop

from subprocess import check_output


if platform.system().lower() == 'darwin':
    from .plugins.stt.engines.snowboy.snowboy_mac import snowboydecoder
elif platform.system().lower() == 'linux':
    from .plugins.stt.engines.snowboy.snowboy_rpi import snowboydecoder


def kill_process(name):
    for rethinkDBprocessID in (map(
            int, check_output(["pidof", name]).split())):
        os.kill(int(rethinkDBprocessID), signal.SIGKILL)


class Conversation(object):

    def __init__(self, mic, speaker, profile, personality):
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.speaker = speaker
        self.profile = profile
        self.personality = personality

        producer_frame_q = multiprocessing.Queue(1)
        producer_gray_q = multiprocessing.Queue(1)
        producer_gray_resized_q = multiprocessing.Queue(1)

        faces_q = multiprocessing.Queue(1)
        faces_rect_q = multiprocessing.Queue(1)
        people_q = multiprocessing.Queue(1)

        mgr = multiprocessing.Manager()
        vision_dict = mgr.dict()
        vision_dict["main_window"] = "Jasper-Vision"
        vision_dict["src"] = 0
        vision_dict["frame_captures"] = 0
        vision_dict['FREQ_DIV'] = 1
        vision_dict["RESIZE_FACTOR"] = 4
        vision_dict["image_path"] = ""
        vision_dict["message"] = ""
        vision_dict['face_name'] = ""
        vision_dict['vision_output_enabled'] = 1

        vision_dict['face_detector'] = 1
        vision_dict['face_recognizer'] = 1

        vision_dict['message_timeout'] = 0

        # for learning
        vision_dict['faceName'] = ''
        vision_dict['training_started'] = 0
        vision_dict['training_captured'] = 0
        vision_dict['new_model_available'] = 0
        vision_dict['number_of_training_images'] = 20

        cam_process = multiprocessing.Process(
            target=camera_loop, args=(
                vision_dict, producer_frame_q, producer_gray_q), daemon=True)
        resizer_process = multiprocessing.Process(
            target=gray_resizing_loop,
            args=(vision_dict, producer_gray_q, producer_gray_resized_q),
            daemon=True)
        detector_process = multiprocessing.Process(
            target=face_detector_loop,
            args=(
                vision_dict,
                producer_gray_q,
                producer_gray_resized_q,
                faces_rect_q,
                faces_q),
            daemon=True)
        learner_process = multiprocessing.Process(
            target=face_learner_loop, args=(vision_dict, faces_q,))
        recognizer_process = multiprocessing.Process(
            target=face_recognizer_loop, args=(
                vision_dict, faces_q, people_q), daemon=True)
        jasper_vision_process = multiprocessing.Process(
            target=jasper_vision_loop,
            args=(
                vision_dict,
                producer_frame_q,
                producer_gray_q,
                producer_gray_resized_q,
                faces_rect_q,
                people_q),
            daemon=True)

        cam_process.start()
        resizer_process.start()
        detector_process.start()
        learner_process.start()
        recognizer_process.start()
        jasper_vision_process.start()

        self._logger.debug("Starting brain for Conversation")

        self.notifier = Notifier(profile, vision_dict)
        self.brain = Brain(mic, speaker, profile, personality,
                           self.notifier, vision_dict)

        wake_word_model = os.path.join(
            paths.SNOWBOY_MODEL_PATH, "Alfred.pmdl")
        wake_from_sleep_model = os.path.join(
            paths.SNOWBOY_MODEL_PATH, "time to wake up.pmdl")

        self.wake_word_detector = snowboydecoder.HotwordDetector(
            wake_word_model, sensitivity=0.4)
        self.wake_from_sleep_detector = snowboydecoder.HotwordDetector(
            wake_from_sleep_model, sensitivity=0.5)

        self._logger.debug("Brain started")

    def handleForever(self):
        if 'first_name' in self.profile:
            salutation = (
                "Hello, I am {}. How can I be of service, {}?".format(
                    self.personality.name,
                    self.profile["first_name"]))
        else:
            salutation = "Hello, I am {}. How can I be of service?".format(
                self.personality.name)

        if self.mic.local_mode:
            self.speaker.clean_and_say(salutation)
            while True:
                inputs = self.mic.activeListenToAllOptions()
                if inputs:
                    self.brain.query(inputs)
                else:
                    self.speaker.clean_and_say("Pardon?")

        elif self.mic.local_mode == False:
            self.profile['sleeping'] = False

            def interrupt_callback():
                pass

            def wake(profile, speaker):
                print("WOKEN FROM SLEEP!")
                profile['sleeping'] = False
                time.sleep(1)
                speaker.clean_and_say(
                    "I am awake, I am Alfred, always at your service!")
                return

            self.speaker.clean_and_say(
                "Adjusting for ambient noise, starting in 3,2,1")
            # using old method
            # self.mic.threshold = self.mic.fetchThreshold()

            # using new method
            # self.mic.adjust_for_ambient_noise()
            self.speaker.clean_and_say("Adjustment done!")
            self.speaker.clean_and_say(salutation)
            callbacks = \
                [
                    lambda: wake(self.profile, self.speaker),
                ]

            while True:
                # Print notifications until empty
                # notifications = self.notifier.getAllNotifications()

                # for notif in notifications:
                #   self._logger.info("Received notification: '%s'", str(notif))

                if not self.profile['sleeping']:
                    # print ("sleeping is false, so listening for alfred")
                    self.wake_word_detector.start(
                        detected_callback=None,
                        interrupt_check=interrupt_callback,
                        sleep_time=1)
                    print("HERE")
                    self.wake_word_detector.terminate()
                    time.sleep(1)
                    threshold = self.mic.fetchThreshold()

                    self.speaker.play_wav_file(
                        paths.data('audio', 'beep_hi.wav'))

                    inputs = self.mic.activeListenToAllOptions(threshold)

                    self.speaker.play_wav_file(
                        paths.data('audio', 'beep_lo.wav'))
                    if inputs:
                        self.brain.query(inputs)
                    else:
                        self.speaker.clean_and_say("Pardon?")
                elif self.profile['sleeping']:
                    # print ("sleeping is True, so listening for time to wake up")
                    self.wake_from_sleep_detector.start(
                        detected_callback=callbacks,
                        interrupt_check=interrupt_callback,
                        sleep_time=0.3)
                    self.wake_from_sleep_detector.terminate()
