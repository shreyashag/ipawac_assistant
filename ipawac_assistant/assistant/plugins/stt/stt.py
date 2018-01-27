#!/usr/bin/env python3
# -*- coding: utf-8-*-

# import urlparse

from .engines.abstract_stt.abstract_stt import AbstractSTTEngine
from .engines.google_stt import GoogleSTT


def get_engine_by_slug(slug=None, args_local=False):
    """
    Returns:
        An STT Engine implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or not isinstance(slug, str):
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                                   engine.SLUG == slug, get_engines()))
    print(selected_engines)
    return GoogleSTT
    if len(list(selected_engines)) == 0:
        raise ValueError("No STT engine found for slug '%s'" % slug)
    else:
        if len(list(selected_engines)) > 1:
            print(("WARNING: Multiple STT engines found for slug '%s'. " +
                   "This is most certainly a bug.") % slug)
        engine = selected_engines[0]
        if not engine.is_available(args_local):
            raise ValueError(("STT engine '%s' is not available (due to " +
                              "missing dependencies, missing " +
                              "dependencies, etc.)") % slug)
        return GoogleSTT


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        print(cls.__subclasses__())
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractSTTEngine))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]
