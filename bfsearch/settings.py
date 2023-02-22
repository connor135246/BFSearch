# settings

import json, logging

from launch import df


settings = {}


def load():
    global settings
    try:
        createFile()
        settings = json.load(open(df("settings.json"), "r", encoding = "UTF-8"))
    except Exception:
        logging.exception("Unable to load settings file 'settings.json'")
        settings = {}
    return settings

def createFile():
    try:
        newConfig = open(df("settings.json"), "x", encoding = "UTF-8")
        newConfig.write("{}")
        newConfig.close()
    except FileExistsError:
        pass

def save():
    global settings
    try:
        json.dump(settings, open(df("settings.json"), "w", encoding = "UTF-8"), indent = 4)
    except Exception:
        logging.exception("Unable to save settings file 'settings.json'")
