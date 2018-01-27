# -*- coding: utf-8-*-
import logging
import pkgutil

# from .plugins import linphone_controller
from assistant.plugins.utilities import paths


class Brain(object):

    def __init__(
            self,
            mic,
            speaker,
            profile,
            personality,
            notifier,
            vision_dict):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        """
        self._logger = logging.getLogger(__name__)
        self.mic = mic
        self.speaker = speaker
        self.profile = profile
        self.notifier = notifier
        self._logger.debug("LOADING MODULES")

        self.modules = self.get_modules()

        self._logger.debug(self.modules)
        self._logger.debug("MODULES Loaded")

        self.vision_dict = vision_dict

        # Brain creates and manages the phone

        # self.linphone=linphoneController.SecurityCamera(username=profile['linphone_id'], password=profile['linphone_password'],
        #    whitelist=['sip:shreyash23@sip.linphone.org', 'sip:nikhil93@sip.linphone.org','sip:amansalehjee@sip.linphone.org'],
        #     camera='Webcam QT Capture: FaceTime HD Camera (Built-in)', snd_capture='AudioUnit: Built-in Microphone (AppleHDAEngineInput:1B,0,1,0:1)',snd_playback='AudioUnit: Built-in Output (AppleHDAEngineOutput:1B,0,1,1:0)')
        # def my_threaded_func(linphoneObject,arg2):
        #     while not linphoneObject.quit:
        #         linphoneObject.core.iterate()
        #         time.sleep(0.03)

        # thread = threading.Thread(target=my_threaded_func, args=(self.linphone,"thread"))
        # thread.daemon=True
        # thread.start()

    @classmethod
    def get_modules(cls):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        logger = logging.getLogger(__name__)
        locations = [paths.MODULE_PATH]
        logger.debug("Looking for modules in: %s",
                     ', '.join(["'%s'" % location for location in locations]))
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except BaseException:
                logger.debug("Skipped module '%s' due to an error.", name,
                             exc_info=True)
            else:
                if hasattr(mod, 'WORDS'):
                    logger.debug("Found module '%s' with words: %r", name,
                                 mod.WORDS)
                    modules.append(mod)
                else:
                    logger.debug("Skipped module '%s' because it misses " +
                                 "the WORDS constant.", name)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules

    def reload_modules():
        self.modules = self.get_modules()

    def query(self, texts):
        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module
        """
        for module in self.modules:
            for text in texts:
                if module.isValid(text):
                    self._logger.debug("'%s' is a valid phrase for module " +
                                       "'%s'", text, module.__name__)
                    try:
                        module.handle(text, self.mic, self.speaker,
                                      self.profile, self.vision_dict)

                        # if re.search('call',text,re.IGNORECASE):ž
                        #     module.handle(text, self.mic, self.profile,self.linphone)
                        # else:
                        #     module.handle(text, self.mic, self.profile)
                    except Exception:
                        self._logger.error('Failed to execute module',
                                           exc_info=True)
                        self.speaker.clean_and_say(
                            "I'm sorry. I had some trouble with " +
                            "that operation. Please try again later.")
                    else:
                        self._logger.debug("Handling of phrase '%s' by " +
                                           "module '%s' completed", text,
                                           module.__name__)
                    finally:
                        return
        self._logger.debug("No module was able to handle any of these " +
                           "phrases: %r", texts)
