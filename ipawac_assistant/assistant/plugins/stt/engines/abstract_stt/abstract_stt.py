from abc import ABCMeta, abstractmethod

# from client import vocabcompiler


class AbstractSTTEngine(object):
    """
    Generic parent class for all STT engines
    """

    __metaclass__ = ABCMeta
    VOCABULARY_TYPE = None

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        config = cls.get_config()
        # if cls.VOCABULARY_TYPE:
        #     vocabulary = cls.VOCABULARY_TYPE(vocabulary_name,
        #                                      path=jasperpath.config(
        #                                          'vocabularies'))
        #     if not vocabulary.matches_phrases(phrases):
        #         vocabulary.compile(phrases)
        #     config['vocabulary'] = vocabulary
        instance = cls(**config)
        return instance

    # @classmethod
    # def get_passive_instance(cls):
    #     phrases = vocabcompiler.get_keyword_phrases()
    #     return cls.get_instance('keyword', phrases)

    @classmethod
    def get_active_instance(cls):
        # phrases = vocabcompiler.get_all_phrases()
        # print (phrases)
        return cls.get_instance()

    @classmethod
    @abstractmethod
    def is_available(cls):
        return True

    @abstractmethod
    def transcribe(self, fp):
        pass
