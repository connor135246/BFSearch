# parsing


from enum import IntEnum
import json
from json.decoder import JSONDecodeError

from bfsearch import core


# data integrity.

class DataFile(IntEnum):
    species = 0
    sets = 1
    trainers = 2

class DataException(Exception):
    def __init__(self, datafile, message, objs):
        self.datafile = datafile
        self.message = message
        self.objs = objs

    def __str__(self):
        return f"'{self.getDataFile()}' error: {self.getFormattedMessage()}"

    def getDataFile(self):
        return f"{self.datafile.name}.json"

    def getFormattedMessage(self):
        return self.message.format(*self.objs)


class FileException(DataException):
    pass

class JsonException(DataException):
    pass

def getFileJson(datafile):
    try:
        return json.load(open("data/" + datafile.name + '.json', 'r', encoding = 'UTF-8'))
    except OSError:
        raise FileException(datafile, "Unable to open file! Is it missing?", [])
    except JSONDecodeError as e:
        raise JsonException(datafile, "JSON Error! {}", [e])
    except TypeError as e:
        raise JsonException(datafile, "JSON Error! {}", [e])


class MissingDataException(DataException):
    pass

def getDictKey(adict, key, datafile, path):
    try:
        return adict[key]
    except KeyError:
        raise MissingDataException(datafile, "Key '{}' missing from json object {}", [key, path])


class InvalidDataException(DataException):
    pass

def verifyInt(value, excep):
    if type(value) is int or (type(value) is str and value.isdecimal()):
        return int(value)
    else:
        raise excep

def verifyList(value, excep):
    if type(value) is list:
        return value
    else:
        raise excep

def verifyDict(value, excep):
    if type(value) is dict:
        return value
    else:
        raise excep

def verifyNonEmptyString(value, excep):
    if type(value) is str:
        value = value.strip()
        if value != '':
            return value
    raise excep

def verifyMany(values, verifier, excep):
    for i in range(len(values)):
        values[i] = verifier.__call__(values[i], excep)
    return values

def verifyLen(value, minimum, excep):
    if len(value) < minimum:
        raise excep
    return value

def verifyLenRange(value, minimum, maximum, excep):
    if len(value) < minimum or len(value) > maximum:
        raise excep
    return value

def verifyEnumValue(value, aenum, excep):
    try:
        return aenum(value)
    except ValueError:
        raise excep

def verifyEnumName(value, aenum, excep):
    try:
        return aenum[value]
    except KeyError:
        raise excep


# parsing data.

def buildData():

    species = {}
    datafile = DataFile.species
    raw_species_data = getFileJson(datafile)

    for species_obj in verifyLen(verifyList(getDictKey(raw_species_data, 'species', datafile, "{HERE}"), InvalidDataException(datafile, "Missing 'species' (object list)", [])), 1, InvalidDataException(datafile, "Empty 'species' (object list)", [])):
        path = '{"species":[{HERE}]}'

        dex = verifyInt(getDictKey(species_obj, 'dex', datafile, path), InvalidDataException(datafile, "Species '{}' is missing 'dex' (number)", [getDictKey(species_obj, 'name', datafile, path)]))

        name = verifyNonEmptyString(getDictKey(species_obj, 'name', datafile, path), InvalidDataException(datafile, "Species with Pokedex number '{}' is missing 'species' (string)", [dex]))

        speed = verifyInt(getDictKey(species_obj, 'speed', datafile, path), InvalidDataException(datafile, "Species '{}' is missing 'speed' (number)", [name]))
        if speed < 1:
            raise InvalidDataException(datafile, "Species '{}' has negative 'speed' (number)", [name])

        abilities = verifyMany(verifyLen(verifyList(getDictKey(species_obj, 'abilities', datafile, path), InvalidDataException(datafile, "Species '{}' is missing 'abilities' (string list)", [name])), 1, InvalidDataException(datafile, "Species '{}' has empty 'abilities' (string list)", [name])), verifyNonEmptyString, InvalidDataException(datafile, "Species '{}' has invalid entry in 'abilities' (string list)", [name]))

        if name in species.keys():
            raise InvalidDataException(datafile, "Duplicate 'species' (string): '{}'", [name])
        species[name] = core.Species(dex, name, speed, abilities)


    sets = {}
    datafile = DataFile.sets
    raw_sets_data = getFileJson(datafile)

    for set_obj in verifyLen(verifyList(getDictKey(raw_sets_data, 'sets', datafile, "{HERE}"), InvalidDataException(datafile, "Missing 'sets' (object list)", [])), 1, InvalidDataException(datafile, "Empty 'sets' (object list)", [])):
        path = '{"sets":[{HERE}]}'

        sid = verifyInt(getDictKey(set_obj, 'id', datafile, path), InvalidDataException(datafile, "Set '{} {}' is missing 'id' (number)", [getDictKey(set_obj, 'species', datafile, path), getDictKey(set_obj, 'set', datafile, path)]))
        for aname in sets.keys():
            for apset in sets[aname].keys():
                if sid == sets[aname][apset].sid:
                    raise InvalidDataException(datafile, "Duplicate 'id' (number): '{}'", [sid])

        name = verifyNonEmptyString(getDictKey(set_obj, 'species', datafile, path), InvalidDataException(datafile, "Set id '{}' is missing 'species' (string)", [sid]))
        if name not in species.keys():
            raise InvalidDataException(datafile, "Set id '{}' uses 'species' named '{}' which was not registered 'species.json'", [sid, name])

        pset = verifyInt(getDictKey(set_obj, 'set', datafile, path), InvalidDataException(datafile, "Set id '{}' is missing 'set' (number)", [sid]))

        nature = verifyEnumName(getDictKey(set_obj, 'nature', datafile, path), core.Nature, InvalidDataException(datafile, "Set id '{}' has invalid 'nature': '{}'", [sid, getDictKey(set_obj, 'nature', datafile, path)]))

        item = verifyNonEmptyString(getDictKey(set_obj, 'item', datafile, path), InvalidDataException(datafile, "Set id '{}' is missing 'item' (string)", [sid]))

        moves = verifyMany(verifyLenRange(verifyList(getDictKey(set_obj, 'moves', datafile, path), InvalidDataException(datafile, "Set id '{}' is missing 'moves' (string list)", [sid])), 1, 4, InvalidDataException(datafile, "Set id '{}' should have 1 to 4 entries in 'moves' (string list)", [sid])), verifyNonEmptyString, InvalidDataException(datafile, "Set id '{}' has invalid entry in 'moves' (string list)", [sid]))

        evs = verifyLenRange(verifyList(getDictKey(set_obj, 'evs', datafile, path), InvalidDataException(datafile, "Set id '{}' is missing 'evs' (string list)", [sid])), 2, 3, InvalidDataException(datafile, "Set id '{}' should have 2 to 3 entries in 'evs' (string list)", [sid]))
        for i in range(len(evs)):
            evs[i] = verifyEnumName(evs[i], core.Stat, InvalidDataException(datafile, "Set id '{}' has invalid entry '{}' in 'evs' (string list)", [sid, evs[i]]))

        if name not in sets.keys():
            sets[name] = {}
        if pset in sets[name].keys():
            raise InvalidDataException(datafile, "Duplicate 'set' (number): '{}' for species '{}'", [pset, name])
        sets[name][pset] = core.PokeSet(sid, species[name], pset, nature, item, moves, core.EVStats(evs))


    trainers = {}
    datafile = DataFile.trainers
    raw_trainer_data = getFileJson(datafile)

    for trainer_obj in verifyLen(verifyList(getDictKey(raw_trainer_data, 'trainers', datafile, "{HERE}"), InvalidDataException(datafile, "Missing'trainers' (object list)", [])), 1, InvalidDataException(datafile, "Empty 'trainers' (object list)", [])):
        path = '{"trainers":[{HERE}]}'

        tid = verifyInt(getDictKey(trainer_obj, 'id', datafile, path), InvalidDataException(datafile, "Trainer '{} {}' is missing 'id' (number)", [getDictKey(trainer_obj, 'class', datafile, path), getDictKey(trainer_obj, 'name', datafile, path)]))
        for atclass in trainers.keys():
            for atname in trainers[atclass].keys():
                if tid == trainers[atclass][atname].tid:
                    raise InvalidDataException(datafile, "Duplicate 'id' (number): '{}'", [tid])

        iv = verifyInt(getDictKey(trainer_obj, 'iv', datafile, path), InvalidDataException(datafile, "Trainer id '{}' is missing 'iv' (number)", [tid]))
        if iv < 0 or iv > 31:
            raise InvalidDataException(datafile, "Trainer id '{}' should have 'iv' (number) between 0 and 31", [tid])

        tclass = verifyNonEmptyString(getDictKey(trainer_obj, 'class', datafile, path), InvalidDataException(datafile, "Trainer id '{}' is missing 'class' (string)", [tid]))

        tname = verifyNonEmptyString(getDictKey(trainer_obj, 'name', datafile, path), InvalidDataException(datafile, "Trainer id '{}' is missing 'name' (string)", [tid]))

        battles = verifyLen(verifyList(getDictKey(trainer_obj, 'battles', datafile, path), InvalidDataException(datafile, "Trainer id '{}' is missing 'battles' (string list)", [tid])), 1, InvalidDataException(datafile, "Trainer id '{}' has empty 'battles' (string list)", [tid]))
        for i in range(len(battles)):
            battles[i] = verifyEnumValue(str(battles[i]), core.BattleNum, InvalidDataException(datafile, "Trainer id '{}' has invalid entry '{}' in 'battles' (string list)", [tid, battles[i]]))

        pokemon = verifyLen(verifyDict(getDictKey(trainer_obj, 'pokemon', datafile, path), InvalidDataException(datafile, "Trainer id '{}' has invalid Pokemon sets object", [tid])), 1, InvalidDataException(datafile, "Trainer id '{}' has empty 'pokemon' (object list)", [tid]))
        pokemondict = {}
        for entry in pokemon.items():
            if entry[0] in sets.keys():
                pokemonsets = verifyLen(verifyList(entry[1], InvalidDataException(datafile, "Trainer id '{}' is missing string list of sets for species '{}'", [tid, entry[0]])), 1, InvalidDataException(datafile, "Trainer id '{}' has empty string list of sets for species '{}'", [tid, entry[0]]))
                if entry[0] not in pokemondict.keys():
                    pokemondict[entry[0]] = {}
                for pokemonset in pokemonsets:
                    if pokemonset in sets[entry[0]].keys():
                        pokemondict[entry[0]][pokemonset] = sets[entry[0]][pokemonset]
                    else:
                        raise InvalidDataException(datafile, "Trainer id '{}' uses set '{} {}' which was not registered 'sets.json'", [tid, entry[0], pokemonset])
            else:
                raise InvalidDataException(datafile, "Trainer id '{}' uses species '{}' which has no sets in 'sets.json'", [tid, entry[0]])

        if tclass not in trainers.keys():
            trainers[tclass] = {}
        if tname in trainers[tclass].keys():
            raise InvalidDataException(datafile, "Duplicate trainer '{} {}'", [tclass, tname])
        trainers[tclass][tname] = core.Trainer(tid, iv, tclass, tname, battles, pokemondict)


    return (species, sets, trainers)
