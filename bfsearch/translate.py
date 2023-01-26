# translate


import glob, json, logging
from json.decoder import JSONDecodeError

from babel import Locale, UnknownLocaleError


def tr(key, args = []):
    return getTranslation(key).format(*args)


baseLang = "en_US"
langFiles = {}
currentLang = baseLang


def getTranslation(key):
    if key in langFiles[currentLang].keys():
        return langFiles[currentLang][key]
    elif currentLang != baseLang and key in langFiles[baseLang]:
        return langFiles[baseLang][key]
    else:
        logging.warning("Translation key '%s' does not exist in language file", key)
        return key


def loadLangFiles():
    langFiles.clear()
    for filename in glob.glob('lang/*.json'):
        try:
            langFile = json.load(open(filename, "r", encoding = "UTF-8"))
            identifier = filename[5:-5]
            if identifier != '':
                langFiles[identifier] = langFile
        # todo: log.
        except OSError as e:
            logging.warning("Unable to open lang file '%s' - %s", filename, e)
        except JSONDecodeError as e:
            logging.warning("Json error when parsing lang file '%s' - %s", filename, e)
        except TypeError as e:
            logging.warning("Json error when parsing lang file '%s' - %s", filename, e)

    if baseLang not in langFiles.keys():
        raise FileNotFoundError("Unable to open base lang file 'lang\\" + baseLang + ".json'")


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
