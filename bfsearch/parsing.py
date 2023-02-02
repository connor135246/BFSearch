# parsing


from enum import IntEnum
import json
from json.decoder import JSONDecodeError

from bfsearch import core
from bfsearch.translate import tr


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
        return tr("parsing.error", [self.getDataFile(), self.getFormattedMessage()])

    def getDataFile(self):
        return f"{self.datafile.name}.json"

    def getFormattedMessage(self):
        return tr(self.message, self.objs)


class FileException(DataException):
    pass

class JsonException(DataException):
    pass

def getFileJson(datafile):
    try:
        return json.load(open("data/" + datafile.name + '.json', 'r', encoding = 'UTF-8'))
    except OSError as e:
        raise FileException(datafile, "parsing.error.file", [e])
    except JSONDecodeError as e:
        raise JsonException(datafile, "parsing.error.json", [e])
    except TypeError as e:
        raise JsonException(datafile, "parsing.error.json", [e])


class MissingDataException(DataException):
    pass

def getDictKey(adict, key, datafile, path):
    try:
        return adict[key]
    except KeyError:
        raise MissingDataException(datafile, "parsing.error.missing_data", [key, path])


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

    for species_obj in verifyLen(verifyList(getDictKey(raw_species_data, 'species', datafile, "{*}"), InvalidDataException(datafile, "parsing.error.species.missing", [])), 1, InvalidDataException(datafile, "parsing.error.species.size", [])):
        path = '{"species":[{*}]}'

        dex = verifyInt(getDictKey(species_obj, 'dex', datafile, path), InvalidDataException(datafile, "parsing.error.species.dex.missing", [getDictKey(species_obj, 'name', datafile, path)]))

        name = verifyNonEmptyString(getDictKey(species_obj, 'name', datafile, path), InvalidDataException(datafile, "parsing.error.species.name.missing", [dex]))

        speed = verifyInt(getDictKey(species_obj, 'speed', datafile, path), InvalidDataException(datafile, "parsing.error.species.speed.missing", [name]))
        if speed < 1:
            raise InvalidDataException(datafile, "parsing.error.species.speed.invalid", [name, speed])

        abilities = verifyMany(verifyLen(verifyList(getDictKey(species_obj, 'abilities', datafile, path), InvalidDataException(datafile, "parsing.error.species.abilities.missing", [name])), 1, InvalidDataException(datafile, "parsing.error.species.abilities.size", [name])), verifyNonEmptyString, InvalidDataException(datafile, "parsing.error.species.abilities.invalid", [name]))

        if name in species.keys():
            raise InvalidDataException(datafile, "parsing.error.species.name.duplicate", [name])
        species[name] = core.Species(dex, name, speed, abilities)


    sets = {}
    datafile = DataFile.sets
    raw_sets_data = getFileJson(datafile)

    for set_obj in verifyLen(verifyList(getDictKey(raw_sets_data, 'sets', datafile, "{*}"), InvalidDataException(datafile, "parsing.error.sets.missing", [])), 1, InvalidDataException(datafile, "parsing.error.sets.size", [])):
        path = '{"sets":[{*}]}'

        sid = verifyInt(getDictKey(set_obj, 'id', datafile, path), InvalidDataException(datafile, "parsing.error.sets.id.missing", [getDictKey(set_obj, 'species', datafile, path), getDictKey(set_obj, 'set', datafile, path)]))
        for aname in sets.keys():
            for apset in sets[aname].keys():
                if sid == sets[aname][apset].sid:
                    raise InvalidDataException(datafile, "parsing.error.sets.id.duplicate", [sid])

        name = verifyNonEmptyString(getDictKey(set_obj, 'species', datafile, path), InvalidDataException(datafile, "parsing.error.sets.species.missing", [sid]))
        if name not in species.keys():
            raise InvalidDataException(datafile, "parsing.error.sets.species.unregistered", [sid, name])

        pset = verifyInt(getDictKey(set_obj, 'set', datafile, path), InvalidDataException(datafile, "parsing.error.sets.set.missing", [sid]))

        nature = verifyEnumName(getDictKey(set_obj, 'nature', datafile, path), core.Nature, InvalidDataException(datafile, "parsing.error.sets.nature.invalid", [sid, getDictKey(set_obj, 'nature', datafile, path)]))

        item = verifyNonEmptyString(getDictKey(set_obj, 'item', datafile, path), InvalidDataException(datafile, "parsing.error.sets.item.missing", [sid]))

        moves = verifyMany(verifyLenRange(verifyList(getDictKey(set_obj, 'moves', datafile, path), InvalidDataException(datafile, "parsing.error.sets.moves.missing", [sid])), 1, 4, InvalidDataException(datafile, "parsing.error.sets.moves.size", [sid])), verifyNonEmptyString, InvalidDataException(datafile, "parsing.error.sets.moves.invalid", [sid]))

        evs = verifyLenRange(verifyList(getDictKey(set_obj, 'evs', datafile, path), InvalidDataException(datafile, "parsing.error.sets.evs.missing", [sid])), 2, 3, InvalidDataException(datafile, "parsing.error.sets.evs.size", [sid]))
        for i in range(len(evs)):
            evs[i] = verifyEnumName(evs[i], core.Stat, InvalidDataException(datafile, "parsing.error.sets.evs.invalid", [sid, evs[i]]))

        if name not in sets.keys():
            sets[name] = {}
        if pset in sets[name].keys():
            raise InvalidDataException(datafile, "parsing.error.sets.set.duplicate", [pset, name])
        sets[name][pset] = core.PokeSet(sid, species[name], pset, nature, item, moves, core.EVStats(evs))


    trainers = {}
    datafile = DataFile.trainers
    raw_trainer_data = getFileJson(datafile)

    for trainer_obj in verifyLen(verifyList(getDictKey(raw_trainer_data, 'trainers', datafile, "{*}"), InvalidDataException(datafile, "parsing.error.trainers.missing", [])), 1, InvalidDataException(datafile, "parsing.error.trainers.size", [])):
        path = '{"trainers":[{*}]}'

        tid = verifyInt(getDictKey(trainer_obj, 'id', datafile, path), InvalidDataException(datafile, "parsing.error.trainers.id.missing", [getDictKey(trainer_obj, 'class', datafile, path), getDictKey(trainer_obj, 'name', datafile, path)]))
        for atclass in trainers.keys():
            for atname in trainers[atclass].keys():
                if tid == trainers[atclass][atname].tid:
                    raise InvalidDataException(datafile, "parsing.error.trainers.id.duplicate", [tid])

        iv = verifyInt(getDictKey(trainer_obj, 'iv', datafile, path), InvalidDataException(datafile, "parsing.error.trainers.iv.missing", [tid]))
        if iv < 0 or iv > 31:
            raise InvalidDataException(datafile, "parsing.error.trainers.iv.invalid", [tid, iv])

        tclass = verifyNonEmptyString(getDictKey(trainer_obj, 'class', datafile, path), InvalidDataException(datafile, "parsing.error.trainers.class.missing", [tid]))

        tname = verifyNonEmptyString(getDictKey(trainer_obj, 'name', datafile, path), InvalidDataException(datafile, "parsing.error.trainers.name.missing", [tid]))

        battles = verifyLen(verifyList(getDictKey(trainer_obj, 'battles', datafile, path), InvalidDataException(datafile, "parsing.error.trainers.battles.missing", [tid])), 1, InvalidDataException(datafile, "parsing.error.trainers.battles.size", [tid]))
        for i in range(len(battles)):
            battles[i] = verifyEnumValue(str(battles[i]), core.BattleNum, InvalidDataException(datafile, "parsing.error.trainers.battles.invalid", [tid, battles[i]]))

        pokemon = verifyLen(verifyDict(getDictKey(trainer_obj, 'pokemon', datafile, path), InvalidDataException(datafile, "parsing.error.trainers.pokemon.missing", [tid])), 1, InvalidDataException(datafile, "parsing.error.trainers.pokemon.size", [tid]))
        pokemondict = {}
        for pname, pentries in pokemon.items():
            if pname in sets.keys():
                pokemonsets = verifyMany(verifyLen(verifyList(pentries, InvalidDataException(datafile, "parsing.error.trainers.pokemon.species.set.missing", [tid, pname])), 1, InvalidDataException(datafile, "parsing.error.trainers.pokemon.species.set.size", [tid, pname])), verifyInt, InvalidDataException(datafile, "parsing.error.trainers.pokemon.species.set.invalid", [tid, pname])) 
                if pname not in pokemondict.keys():
                    pokemondict[pname] = {}
                for pokemonset in pokemonsets:
                    if pokemonset in sets[pname].keys():
                        pokemondict[pname][pokemonset] = sets[pname][pokemonset]
                    else:
                        raise InvalidDataException(datafile, "parsing.error.trainers.pokemon.species.set.unregistered", [tid, pname, pokemonset])
            else:
                raise InvalidDataException(datafile, "parsing.error.trainers.pokemon.species.unregistered", [tid, pname])

        if tclass not in trainers.keys():
            trainers[tclass] = {}
        if tname in trainers[tclass].keys():
            raise InvalidDataException(datafile, "parsing.error.trainers.duplicate", [tclass, tname])
        trainers[tclass][tname] = core.Trainer(tid, iv, tclass, tname, battles, pokemondict)


    return (species, sets, trainers)
