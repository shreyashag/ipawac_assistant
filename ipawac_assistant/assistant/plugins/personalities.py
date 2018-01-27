from abc import ABCMeta, abstractmethod
import logging


class AbstractPersonality(object):
    """
    Generic parent class for all Personalities
    """
    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        config = cls.get_config()
        instance = cls(**config)
        return instance

    @classmethod
    @abstractmethod
    def is_available(cls):
        return True

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)

    # @abstractmethod
    # def say(self, phrase, *args):
    #     pass

    # def clean_and_say(self, phrase,OPTIONS=" -vdefault+m3 -p 40 -s 160 --stdout > say.wav"):
    #     # alter phrase before speaking
    #     phrase = alteration.clean(phrase)
    #     self.say(phrase)
    #     print ("JASPER: "+phrase)


class Alfred(AbstractPersonality):
    """
    Uses the eSpeak speech synthesizer included in the Jasper disk image
    Requires espeak to be available
    """

    SLUG = "Alfred"
    name = "Alfred"
    gender = "Male"
    age = 35

    def __init__(self):
        super(self.__class__, self).__init__()


class Yoda(AbstractPersonality):
    """
    Uses the eSpeak speech synthesizer included in the Jasper disk image
    Requires espeak to be available
    """

    SLUG = "Yoda"
    name = "Yoda"
    gender = "Hmmm?"
    age = 1000

    def __init__(self):
        super(self.__class__, self).__init__()


class Siri(AbstractPersonality):
    """
    Uses the eSpeak speech synthesizer included in the Jasper disk image
    Requires espeak to be available
    """

    SLUG = "Siri"
    name = "Siri"
    gender = "Female"
    age = 32

    def __init__(self):
        super(self.__class__, self).__init__()


def get_default_personality_slug():
    return 'Alfred'


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [personality for personality in
            list(get_subclasses(AbstractPersonality))
            if hasattr(personality, 'SLUG') and personality.SLUG]


def get_personality_by_slug(slug=None):
    """
    Returns:
        A speaker implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or not isinstance(slug, str):
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                                   engine.SLUG == slug, get_engines()))
    if len(selected_engines) == 0:
        raise ValueError("No Personalities engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print("WARNING: Multiple Personalities found for slug '%s'. " +
                  "This is most certainly a bug." % slug)
        engine = selected_engines[0]

        return engine
