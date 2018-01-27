import pipes
import subprocess
import tempfile
from client.plugins.utilities import diagnose
from ..abstract import AbstractTTSEngine


class MimicTTS(AbstractTTSEngine):
    """
    Dummy TTS engine that logs phrases with INFO level instead of synthesizing
    speech.
    """

    SLUG = "mimic-tts"

    @classmethod
    def is_available(cls):
        return (diagnose.check_executable('mimic'))

    def say(self, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        cmd = ['mimic', '-voice', 'rms', str(phrase)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)

    # def play(self, filename):
    #     cmd = ['afplay', str(filename)]
    #     self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
    #                                                  for arg in cmd]))
    #     with tempfile.TemporaryFile() as f:
    #         subprocess.call(cmd, stdout=f, stderr=f)
    #         f.seek(0)
    #         output = f.read()
    #         if output:
    #             self._logger.debug("Output was: '%s'", output)
