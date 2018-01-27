from ..abstract import AbstractTTSEngine


class LocalTTS(AbstractTTSEngine):
    """
    Uses the eSpeak speech synthesizer included in the Jasper disk image
    Requires espeak to be available
    """

    SLUG = "local-tts"

    def __init__(self):
        super(self.__class__, self).__init__()

    @classmethod
    def is_available(cls):
        return (True)

    def say(self, phrase):
        pass
