# parsing


from enum import IntEnum
import json
from json.decoder import JSONDecodeError

from bfsearch import core, data
from bfsearch.translate import tr


# data integrity.

class DataFile(IntEnum):
    species = 0
    sets = 1
    trainers = 2
    hall_sets = 3

class DataException(Exception):
    def __init__(self, datafile, messagepart, *args):
        self.datafile = datafile
        self.message = "parsing.error." + messagepart
        self.args = args

    def __str__(self):
        return tr("parsing.error", self.getDataFile(), self.getFormattedMessage())

    def getDataFile(self):
        return f"{self.datafile.name}.json"

    def getFormattedMessage(self):
        return tr(self.message, *self.args)


class FileException(DataException):
    pass

class JsonException(DataException):
    pass

def getFileJson(datafile):
    try:
        with open("data/" + datafile.name + '.json', 'r', encoding = 'UTF-8') as file:
            return json.load(file)
    except OSError as e:
        raise FileException(datafile, "file", e)
    except JSONDecodeError as e:
        raise JsonException(datafile, "json", e)
    except TypeError as e:
        raise JsonException(datafile, "json", e)


class MissingDataException(DataException):
    pass

def getDictKey(adict, key, datafile, path):
    try:
        return adict[key]
    except KeyError:
        raise MissingDataException(datafile, "missing_data", key, path)


class InvalidDataException(DataException):
    pass

def verifyInt(value, excep):
    if type(value) is int or (type(value) is str and value.isdecimal()):
        return int(value)
    raise excep

def verifyIntPos(value, excep):
    value = verifyInt(value, excep)
    if value > 0:
        return value
    raise excep

def verifyIntRange(value, minimum, maximum, excep):
    value = verifyInt(value, excep)
    if value < minimum or value > maximum:
        raise excep
    return value

def verifyLen(value, minimum, excep):
    if len(value) < minimum:
        raise excep
    return value

def verifyLenRange(value, minimum, maximum, excep):
    if len(value) < minimum or len(value) > maximum:
        raise excep
    return value

def verifyList(value, excep):
    if type(value) is list:
        return value
    raise excep

def verifyNonEmptyList(value, excep):
    return verifyLen(verifyList(value, excep), 1, excep)

def verifyDict(value, excep):
    if type(value) is dict:
        return value
    else:
        raise excep

def verifyNonEmptyDict(value, excep):
    return verifyLen(verifyDict(value, excep), 1, excep)

def verifyValidString(value, excep):
    if type(value) is str:
        value = value.strip()
        if value != '' and value != data.emptyKey:  # data.emptyKey is reserved
            return value
    raise excep

def verifyMany(values, verifier, excep):
    for i in range(len(values)):
        values[i] = verifier.__call__(values[i], excep)
    return values

def verifyEnumValue(value, aenum, excep):
    try:
        return aenum(value)
    except ValueError:
        raise excep

def verifyEnumName(value, aenum, excep):
    try:
        return aenum[str(value)]
    except KeyError:
        raise excep

def verifyFunc(value, verifier, excep):
    try:
        return verifier(value)
    except ValueError:
        raise excep


# parsing data.

def buildData():

    # shorthand
    def IDE(datafile, messagepart, *args):
        return InvalidDataException(datafile, messagepart, *args)

    # shorthand
    trO = tr("parsing.error.piece.object")
    trOL = tr("parsing.error.piece.object_list")
    trS = tr("parsing.error.piece.string")
    trSL = tr("parsing.error.piece.string_list")
    trPN = tr("parsing.error.piece.positive_number")

    species = {}
    datafile = DataFile.species
    raw_species_data = getFileJson(datafile)

    for species_obj in verifyNonEmptyList(getDictKey(raw_species_data, 'species', datafile, "{*}"), IDE(datafile, "datafile", 'species', trOL)):
        path = '{"species":[{*}]}'

        dex = verifyIntPos(getDictKey(species_obj, 'dex', datafile, path), IDE(datafile, "species.missing", getDictKey(species_obj, 'name', datafile, path), 'dex', trPN))

        name = verifyValidString(getDictKey(species_obj, 'name', datafile, path), IDE(datafile, "species.missing.by_dex", dex, 'name', trS))

        types = verifyLenRange(verifyList(getDictKey(species_obj, 'types', datafile, path), IDE(datafile, "species.missing", name, 'types', trSL)), 1, 2, IDE(datafile, "species.size", name, 1, 2, 'types', trSL))
        for i in range(len(types)):
            types[i] = verifyEnumName(types[i], core.Type, IDE(datafile, "species.invalid_entry.of", name, types[i], 'types', trSL))

        speed = verifyIntPos(getDictKey(species_obj, 'speed', datafile, path), IDE(datafile, "species.missing", name, 'speed', trPN))

        abilities = verifyMany(verifyNonEmptyList(getDictKey(species_obj, 'abilities', datafile, path), IDE(datafile, "species.empty", name, 'abilities', trSL)), verifyValidString, IDE(datafile, "species.invalid_entry", name, 'abilities', trSL))
        if len(set(abilities)) < len(abilities):
            raise IDE(datafile, "species.duplicate_entry", name, 'abilities', trSL)

        if name in species.keys():
            raise IDE(datafile, "species.duplicate", 'name', name)
        species[name] = core.Species(dex, name, types, speed, abilities)


    sets = {}
    datafile = DataFile.sets
    raw_sets_data = getFileJson(datafile)

    for set_obj in verifyNonEmptyList(getDictKey(raw_sets_data, 'sets', datafile, "{*}"), IDE(datafile, "datafile", 'sets', trOL)):
        path = '{"sets":[{*}]}'

        sid = verifyIntPos(getDictKey(set_obj, 'id', datafile, path), IDE(datafile, "sets.missing.by_name", getDictKey(set_obj, 'species', datafile, path), getDictKey(set_obj, 'set', datafile, path), 'id', trPN))
        for aname in sets.keys():
            for apset in sets[aname].keys():
                if sid == sets[aname][apset].sid:
                    raise IDE(datafile, "sets.duplicate", 'id', sid)

        setgroup = verifyEnumName(getDictKey(set_obj, 'set_group', datafile, path), core.SetGroup, IDE(datafile, "sets.invalid", sid, 'set_group', getDictKey(set_obj, 'set_group', datafile, path)))

        name = verifyValidString(getDictKey(set_obj, 'species', datafile, path), IDE(datafile, "sets.missing", sid, 'species', trS))
        if name not in species.keys():
            raise IDE(datafile, "sets.unregistered", sid, 'species', name)

        pset = verifyIntPos(getDictKey(set_obj, 'set', datafile, path), IDE(datafile, "sets.missing", sid, 'set', trPN))
        if pset != setgroup.setNumber():
            raise IDE(datafile, "sets.mismatched", sid, 'set', setgroup.setNumber(), 'set_group', pset)

        nature = verifyEnumName(getDictKey(set_obj, 'nature', datafile, path), core.Nature, IDE(datafile, "sets.invalid", sid, 'nature', getDictKey(set_obj, 'nature', datafile, path)))

        item = verifyValidString(getDictKey(set_obj, 'item', datafile, path), IDE(datafile, "sets.missing", sid, 'item', trS))

        moves = verifyMany(verifyLenRange(verifyList(getDictKey(set_obj, 'moves', datafile, path), IDE(datafile, "sets.missing", sid, 'moves', trSL)), 1, 4, IDE(datafile, "sets.size", sid, 1, 4, 'moves', trSL)), verifyValidString, IDE(datafile, "sets.invalid_entry", sid, 'moves', trSL))
        if len(set(moves)) < len(moves):
            raise IDE(datafile, "sets.duplicate_entry", name, 'moves', trSL)

        evs = verifyLenRange(verifyList(getDictKey(set_obj, 'evs', datafile, path), IDE(datafile, "sets.missing", sid, 'evs', trSL)), 2, 3, IDE(datafile, "sets.size", sid, 2, 3, 'evs', trSL))
        for i in range(len(evs)):
            evs[i] = verifyEnumName(evs[i], core.Stat, IDE(datafile, "sets.invalid_entry.of", sid, evs[i], 'evs', trSL))
        if len(set(evs)) < len(evs):
            raise IDE(datafile, "sets.duplicate_entry", name, 'evs', trSL)

        if name not in sets.keys():
            sets[name] = {}
        if pset in sets[name].keys():
            raise IDE(datafile, "sets.duplicate.for_species", 'set', pset, name)
        sets[name][pset] = core.PokeSet(sid, setgroup, species[name], pset, nature, item, moves, core.EVStats(evs))


    trainers = {}
    datafile = DataFile.trainers
    raw_trainer_data = getFileJson(datafile)

    for trainer_obj in verifyNonEmptyList(getDictKey(raw_trainer_data, 'trainers', datafile, "{*}"), IDE(datafile, "datafile", 'trainers', trOL)):
        path = '{"trainers":[{*}]}'

        tid = verifyIntPos(getDictKey(trainer_obj, 'id', datafile, path), IDE(datafile, "trainers.missing.by_name", getDictKey(trainer_obj, 'class', datafile, path), getDictKey(trainer_obj, 'name', datafile, path), 'id', trPN))
        for atclass in trainers.keys():
            for atname in trainers[atclass].keys():
                if tid == trainers[atclass][atname].tid:
                    raise IDE(datafile, "trainers.duplicate", 'id', tid)

        iv = verifyIntRange(getDictKey(trainer_obj, 'iv', datafile, path), 0, 31, IDE(datafile, "trainers.missing.range", tid, 'iv', 0, 31))

        tclass = verifyValidString(getDictKey(trainer_obj, 'class', datafile, path), IDE(datafile, "trainers.missing", tid, 'class', trS))

        tname = verifyValidString(getDictKey(trainer_obj, 'name', datafile, path), IDE(datafile, "trainers.missing", tid, 'name', trS))

        battles = verifyNonEmptyList(getDictKey(trainer_obj, 'battles', datafile, path), IDE(datafile, "trainers.empty", tid, 'battles', trSL))
        for i in range(len(battles)):
            battles[i] = verifyEnumValue(str(battles[i]), core.BattleNum, IDE(datafile, "trainers.invalid_entry.of", tid, battles[i], 'battles', trSL))

        pokemon = verifyNonEmptyDict(getDictKey(trainer_obj, 'pokemon', datafile, path), IDE(datafile, "trainers.empty", tid, 'pokemon', trOL))
        pokemondict = {}
        for pname, pentries in pokemon.items():
            if pname in sets.keys():
                pokemonsets = verifyMany(verifyNonEmptyList(pentries, IDE(datafile, "trainers.empty.set_list", tid, pname)), verifyIntPos, IDE(datafile, "trainers.invalid.set_list", tid, pname))
                if pname not in pokemondict.keys():
                    pokemondict[pname] = {}
                for pokemonset in pokemonsets:
                    if pokemonset in sets[pname].keys():
                        pokemondict[pname][pokemonset] = sets[pname][pokemonset]
                    else:
                        raise IDE(datafile, "trainers.unregistered.set", tid, pname, pokemonset)
            else:
                raise IDE(datafile, "trainers.unregistered.species", tid, pname)

        if tclass not in trainers.keys():
            trainers[tclass] = {}
        if tname in trainers[tclass].keys():
            raise IDE(datafile, "trainers.duplicate.for_class", 'name', tname, tclass)
        trainers[tclass][tname] = core.Trainer(tid, iv, tclass, tname, battles, pokemondict)


    hall_sets = {}
    datafile = DataFile.hall_sets
    raw_hall_sets_data = getFileJson(datafile)

    for hall_set_obj in verifyNonEmptyList(getDictKey(raw_hall_sets_data, 'hall_sets', datafile, "{*}"), IDE(datafile, "datafile", 'hall_sets', trOL)):
        path = '{"hall_sets":[{*}]}'

        hid = verifyIntPos(getDictKey(hall_set_obj, 'hall_id', datafile, path), IDE(datafile, "hall_sets.missing.by_name", getDictKey(hall_set_obj, 'species', datafile, path), 'hall_id', trPN))
        for aname in hall_sets.keys():
            if hid == hall_sets[aname].hid:
                raise IDE(datafile, "hall_sets.duplicate", 'hall_id', hid)

        hallsetgroup = verifyFunc(getDictKey(hall_set_obj, 'hall_set_group', datafile, path), core.HallSetGroup.fromFullName, IDE(datafile, "hall_sets.invalid", hid, 'hall_set_group', getDictKey(hall_set_obj, 'hall_set_group', datafile, path)))

        name = verifyValidString(getDictKey(hall_set_obj, 'species', datafile, path), IDE(datafile, "hall_sets.missing", hid, 'species', trS))
        if name not in species.keys():
            raise IDE(datafile, "hall_sets.unregistered", hid, 'species', name)

        nature = verifyEnumName(getDictKey(hall_set_obj, 'nature', datafile, path), core.Nature, IDE(datafile, "hall_sets.invalid", hid, 'nature', getDictKey(hall_set_obj, 'nature', datafile, path)))

        item = verifyValidString(getDictKey(hall_set_obj, 'item', datafile, path), IDE(datafile, "hall_sets.missing", hid, 'item', trS))

        moves = verifyMany(verifyLenRange(verifyList(getDictKey(hall_set_obj, 'moves', datafile, path), IDE(datafile, "hall_sets.missing", hid, 'moves', trSL)), 1, 4, IDE(datafile, "hall_sets.size", hid, 1, 4, 'moves', trSL)), verifyValidString, IDE(datafile, "hall_sets.invalid_entry", hid, 'moves', trSL))
        if len(set(moves)) < len(moves):
            raise IDE(datafile, "hall_sets.duplicate_entry", name, 'moves', trSL)

        evs = verifyLenRange(verifyList(getDictKey(hall_set_obj, 'evs', datafile, path), IDE(datafile, "hall_sets.missing", hid, 'evs', trSL)), 2, 3, IDE(datafile, "hall_sets.size", hid, 2, 3, 'evs', trSL))
        for i in range(len(evs)):
            evs[i] = verifyEnumName(evs[i], core.Stat, IDE(datafile, "hall_sets.invalid_entry.of", hid, evs[i], 'evs', trSL))
        # TODO: Battle Hall Flareon has only 1 EV in the data??? Is this a typo? For now, I've given it SpA twice and made this exception.
        if name != 'Flareon':
            if len(set(evs)) < len(evs):
                raise IDE(datafile, "hall_sets.duplicate_entry", name, 'evs', trSL)

        if len(evs) == 3:
            print(hid)

        if name in hall_sets.keys():
            raise IDE(datafile, "hall_sets.duplicate", 'species', name)
        hall_sets[name] = core.HallPokeSet(hid, hallsetgroup, species[name], nature, item, moves, core.EVStats(evs))


    return (species, sets, trainers, hall_sets)
