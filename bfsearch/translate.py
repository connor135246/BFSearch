# translate


import glob, json, logging, os
from json.decoder import JSONDecodeError

from babel import Locale, UnknownLocaleError

from bfsearch import settings


def tr(key, *args):
    return getTranslation(key).format(*args)


settingsKey = "previous_language"
defaultLang = "en_US"
langFiles = {}
currentLang = defaultLang


def getTranslation(key):
    if key in langFiles[currentLang].keys():
        return langFiles[currentLang][key]
    elif currentLang != defaultLang and key in langFiles[defaultLang].keys():
        logging.info("Translation key '%s' does not exist in current language file, using default language file instead", key)
        return langFiles[defaultLang][key]
    else:
        logging.warning("Translation key '%s' does not exist", key)
        return key


def loadLangFiles():
    global settingsKey, defaultLang, langFiles, currentLang
    currentLang = settings.settings.get(settingsKey, defaultLang)

    langFiles.clear()
    os.makedirs("lang", exist_ok = True)
    for filename in glob.glob('lang/*.json'):
        try:
            langFile = json.load(open(filename, "r", encoding = "UTF-8"))
            identifier = filename[5:-5]
            if identifier != '':
                langFiles[identifier] = langFile
        except OSError as e:
            logging.warning("Unable to open lang file '%s' - %s", filename, e)
        except JSONDecodeError as e:
            logging.warning("Json error when parsing lang file '%s' - %s", filename, e)
        except TypeError as e:
            logging.warning("Json error when parsing lang file '%s' - %s", filename, e)

    if defaultLang not in langFiles.keys():
        raise FileNotFoundError("Missing default language file 'lang\\" + defaultLang + ".json'")

    if currentLang not in langFiles.keys():
        logging.warning("Missing expected previous language file 'lang\\" + currentLang + ".json', going back to default")
        currentLang = defaultLang
        settings.settings[settingsKey] = defaultLang
        settings.save()


def langs():
    return langFiles.keys()

def prettyLangsDict():
    prettyDict = {}
    for lang in langs():
        try:
            locale = Locale.parse(lang)
            prettyName = locale.get_display_name(locale)
        except UnknownLocaleError:
            prettyName = lang
        except ValueError:
            prettyName = lang
        prettyDict[prettyName + " [" + lang + ".json]"] = lang
    return prettyDict

def currentLangIndex():
    try:
        return list(langs()).index(currentLang)
    except ValueError:
        return 0
