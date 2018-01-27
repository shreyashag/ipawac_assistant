# -*- coding: utf-8-*-
import os

# Jasper main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.pardir, os.pardir, os.pardir))
CONFIG_PATH = os.path.expanduser(os.getenv('IPAWAC_CONFIG'))

PLUGIN_PATH = os.path.normpath(os.path.join(APP_PATH, 'assistant'))

LIB_PATH = os.path.join(APP_PATH, "client")


MODULE_PATH = os.path.join(APP_PATH, "assistant-modules")


DATA_PATH = os.path.join(APP_PATH, "static")


APP_CREDENTIALS_PATH = os.path.join(
    LIB_PATH, "application-credentials")

USER_CREDENTIALS_PATH = CONFIG_PATH

AUDIO_PATH = os.path.join(DATA_PATH, "audio")

RETHINKDB_DATA_PATH = os.path.join(DATA_PATH, "rethinkDB")

MODELS_PATH = os.path.join(DATA_PATH, "models")

SNOWBOY_MODEL_PATH = os.path.join(MODELS_PATH, "snowboy-models")

HAAR_PATH = os.path.join(MODELS_PATH, "haarcascades")
FRONT_CASCADE_PATH = os.path.join(
    HAAR_PATH, "haarcascade_frontalface_default.xml")
FRONT_LPB_CASCADE_PATH = os.path.join(
    HAAR_PATH, "lbpcascade_frontalface_improved.xml")
RIGHT_LPB_CASCADE_PATH = os.path.join(HAAR_PATH, "lbpcascade_profileface.xml")

FACE_MODELS = os.path.join(MODELS_PATH, 'face-models')
FACE_FISCHER_MODEL = os.path.join(FACE_MODELS, 'fisher_trained_data.xml')


folder_paths = [APP_PATH, CONFIG_PATH,
                PLUGIN_PATH, LIB_PATH,
                DATA_PATH, MODULE_PATH,
                USER_CREDENTIALS_PATH, AUDIO_PATH,
                RETHINKDB_DATA_PATH, MODELS_PATH,
                SNOWBOY_MODEL_PATH, HAAR_PATH,
                FRONT_CASCADE_PATH, FRONT_LPB_CASCADE_PATH,
                RIGHT_LPB_CASCADE_PATH, FACE_MODELS,
                FACE_FISCHER_MODEL, '', ]

# for d in folder_paths:
#     print(d)
#     if not os.path.isdir(d):
#         print(d + " does not exist")

if not os.path.isdir(FACE_MODELS):
    os.makedirs(FACE_MODELS)
if not os.path.isfile(FACE_FISCHER_MODEL):
    file = open(FACE_FISCHER_MODEL, 'w+')


IMAGES_FOLDER = os.path.join(DATA_PATH, "images")
FACES_PATH = os.path.join(IMAGES_FOLDER, "faces")
WEATHER_ICONS = os.path.join(IMAGES_FOLDER, "weather-icons-png")


if not os.path.isdir(RETHINKDB_DATA_PATH):
    os.makedirs(RETHINKDB_DATA_PATH)
if not os.path.isdir(FACES_PATH):
    os.makedirs(FACES_PATH)
if not os.path.isdir(WEATHER_ICONS):
    os.makedirs(WEATHER_ICONS)


def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    return os.path.join(DATA_PATH, *fname)
