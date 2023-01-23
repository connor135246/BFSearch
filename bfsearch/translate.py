# translate


import glob

import json
from json.decoder import JSONDecodeError


def tr(key, args = []):
    return getTranslation(key).format(*args)


_defaultLang = "lang\\en_US.json"
_currentLang = _defaultLang
_langFiles = {}


def getTranslation(key):
    if key in _langFiles[_currentLang].keys():
        return _langFiles[_currentLang][key]
    elif _currentLang != _defaultLang and key in _langFiles[_defaultLang]:
        return _langFiles[_defaultLang][key]
    else:
        return key


def loadLangFiles():
    _langFiles.clear()
    for filename in glob.glob('lang/*.json'):
        try:
            langFile = json.load(open(filename, "r", encoding = "UTF-8"))
            _langFiles[filename] = langFile
        # todo: log.
        except OSError:
            pass
        except JSONDecodeError as e:
            pass
        except TypeError as e:
            pass

    if _defaultLang not in _langFiles.keys():
        raise Exception("Unable to open default lang file '" + _defaultLang + "'!")


def availableLangs():
    return _langFiles.keys()


def swapLangFile(newLang):
    if newLang in availableLangs():
        _currentLang = newLang
    else:
        print("Not an available language!")
