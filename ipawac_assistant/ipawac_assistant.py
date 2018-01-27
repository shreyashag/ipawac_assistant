#!/usr/bin/env python2
# -*- coding: utf-8-*-

import argparse
import logging
import multiprocessing
import os
import sys
import pexpect
import yaml


from assistant import Conversation
from assistant.plugins import personalities
from assistant.plugins.stt import stt
from assistant.plugins.tts import tts
from assistant.plugins.utilities import paths, diagnose, populate

# Add paths.LIB_PATH to sys.path
sys.path.append(paths.LIB_PATH)
parser = argparse.ArgumentParser(description='Jasper Voice Control Center')
parser.add_argument('--local', action='store_true',
                    help='Use text input instead of a real microphone')
parser.add_argument('--no-network-check', action='store_true',
                    help='Disable the network connection check')
parser.add_argument('--diagnose', action='store_true',
                    help='Run diagnose and exit')
parser.add_argument('--debug', action='store_true', help='Show debug messages')
args = parser.parse_args()

if args.local:
    from assistant.local_mic import Mic
    local_mode = True
else:
    from assistant.mic import Mic
    local_mode = False


class Jasper(object):
    def __init__(self):

        # self.vision=vision
        self._logger = logging.getLogger(__name__)

        # Create config dir if it does not exist yet
        if not os.path.exists(paths.CONFIG_PATH):
            try:
                os.makedirs(paths.CONFIG_PATH)
            except OSError:
                self._logger.error("Could not create config dir: '%s'",
                                   paths.CONFIG_PATH, exc_info=True)
                raise

        # Check if config dir is writable
        if not os.access(paths.CONFIG_PATH, os.W_OK):
            self._logger.critical("Config dir %s is not writable. Jasper " +
                                  "won't work correctly.",
                                  paths.CONFIG_PATH)

        configfile = paths.config('profile.yml')
        print(configfile)

        if os.path.exists(configfile):
            pass
        else:
            return
            # run profile populator, warn that profile was not found
            populate.populateProfile()

        # Read config
        self._logger.debug("Trying to read config file: '%s'", configfile)

        try:
            with open(configfile, "r") as f:
                self.config = yaml.safe_load(f)
        except OSError:
            self._logger.error("Can't open config file: '%s'", configfile)
            raise

        try:
            stt_engine_slug = self.config['stt_engine']
        except KeyError:
            stt_engine_slug = 'sphinx'
            logger.warning("stt_engine not specified in profile, defaulting " +
                           "to '%s'", stt_engine_slug)
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug, local_mode)

        try:
            tts_engine_slug = self.config['tts_engine']
        except KeyError:
            tts_engine_slug = tts.get_default_engine_slug()
            logger.warning("tts_engine not specified in profile, defaulting " +
                           "to '%s'", tts_engine_slug)
        if local_mode:
            tts_engine_class = tts.get_engine_by_slug('local-tts')
        else:
            tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        try:
            personality_slug = self.config['personality']
        except KeyError:
            personality_slug = personalities.get_default_personality_slug()
            logger.warning(
                "personality not specified in profile, defaulting " +
                "to '%s'",
                personality_slug)

        self.personality = personalities.get_personality_by_slug(
            personality_slug)

        # print (dir(self.personality))
        # Initialize Mic
        # Customize voice according to personality maybe?
        self.speaker = tts_engine_class.get_instance()

        self.mic = Mic(stt_engine_class.get_active_instance(), local_mode)

    def run(self):
        conversation = Conversation(
            self.mic, self.speaker, self.config, self.personality)
        conversation.handleForever()


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    print("********************************************************************************")
    print("********************************************************************************")
    print("*          Intelligent Personal Assistant with Alternative Communication       *")
    print("*            (c) 2017 Shreyash Agarwal, Nikhil Suresh and Vinut Naganath       *")
    print("*            Batch Number 10, Information Science Engineering                  *")
    print("*        Final year project in M.S.Ramaiah Institute of Technology, 2017       *")
    print("********************************************************************************")

    logger = multiprocessing.log_to_stderr()

    # logger.setLevel(multiprocessing.SUBDEBUG)
    logging.basicConfig()
    logger = logging.getLogger()
    # logger.getChild("client.stt").setLevel(logging.INFO)
    logger.setLevel(logging.WARNING)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if not args.no_network_check and not diagnose.check_network_connection():
        logger.warning("Network not connected. This may prevent Jasper from " +
                       "running properly.")

    if args.diagnose:
        failed_checks = diagnose.run()
        sys.exit(0 if not failed_checks else 1)

    try:
        # Start RethinkDB
        rethinkdbprocess = pexpect.spawn(
            "rethinkdb -d {} -n JasperAssistantServer --bind 127.0.0.1".format(
                paths.RETHINKDB_DATA_PATH,))
        rethinkdbprocess.expect(
            'Listening on http addresses: 127.0.0.1', timeout=None)

        from assistant.plugins import rethinkdb_connector

        try:
            rethinkdb_connector.instantiate_if_not_exists()
        except BaseException:
            pass
        diagnose.kill_process("vlc")
        command = "vlc --extraintf telnet --telnet-password admin --lua-config \"telnet={host=\'localhost:9000\'}\""
        player = pexpect.spawn(command)
        app = Jasper()
    except Exception:
        logger.error("Error occured!", exc_info=True)
        sys.exit(1)
    app.run()
# -*- coding: utf-8 -*-

"""Main module."""
