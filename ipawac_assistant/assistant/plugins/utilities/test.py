import os

# Jasper main directory
PLUGINS_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        os.pardir))
APP_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(
            os.path.abspath(PLUGINS_PATH)),
        os.pardir))
print(APP_PATH)
