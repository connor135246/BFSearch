# settings

import json, logging


settings = {}


def load():
    try:
        createFile()
        with open("settings.json", "r", encoding = "UTF-8") as file:
            settings.clear()
            settings.update(json.load(file))
    except Exception:
        logging.exception("Unable to load settings file 'settings.json'")
        settings.clear()
    return settings

def createFile():
    try:
        with open("settings.json", "x", encoding = "UTF-8") as newConfig:
            newConfig.write("{}")
    except FileExistsError:
        pass
    except Exception:
        logging.exception("Unable to create settings file 'settings.json'")

def save():
    try:
        with open("settings.json", "w", encoding = "UTF-8") as file:
            json.dump(settings, file, indent = 4)
    except Exception:
        logging.exception("Unable to save settings file 'settings.json'")
