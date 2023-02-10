import os
from configparser import ConfigParser
from pathlib import Path
import re
from vault.pw import pw

configur = ConfigParser()
working_path = Path(os.getcwd())
print("working path: " + str(working_path.resolve()))
config_path = Path(re.findall(r'.*(?<=BigBagTagger)', str(working_path.resolve()))[0] + "/config.ini")
print("config_path: " + str(config_path))
configur.read(config_path)

""" config part headers """
APP = 'app'
LOGGING = 'logging'

class App:
    APP_NAME = "BigbagTagger"
    TMP_PATH = Path(configur.get(APP, 'TMP_PATH'))
    LOG_PATH = Path(configur.get(APP, 'LOG_PATH'))
    PLAYLIST_PATH = Path(configur.get(APP, 'PLAYLIST_PATH'))
    DO_ALL = configur.getboolean(APP, 'DO_ALL')
class Logging:
    USER = configur.get(LOGGING, 'USER')
    TO = configur.get(LOGGING, 'TO')
    HOST = configur.get(LOGGING, 'HOST')
    SUBJECT = configur.get(LOGGING, 'SUBJECT')
    PASSWORD = pw
