# data


from operator import itemgetter

from bfsearch import core
from bfsearch import parsing


# data container.

class DataHolder(object):
    def __init__(self):
        #true if it has data!
        self.isEmpty = True
        
        # dictionary of '{name}' to Species
        self.species = {}
        # dictionary of '{name}' to dictionary of '{pset}' to Pokeset
        self.sets = {}
        # dictionary of '{tclass}' to dictionary of '{tname}' to Trainer
        self.trainers = {}

    # tries to build data! returns error message.
    def fillerup(self):
        try:
            self.species, self.sets, self.trainers = parsing.buildData()
            self.isEmpty = False
            return ""
        except parsing.DataException as e:
            self.species, self.sets, self.trainers = {}, {}, {}
            self.isEmpty = True
            return e.__class__.__name__ + ": " + str(e)


# general methods.

def sorted_dict(adict):
    return dict(sorted(adict.items(), key = itemgetter(0)))

def sorted_double_dict(doubledict):
    sorteddoubledict = {}
    for adict in doubledict.items():
        sorteddoubledict[adict[0]] = sorted_dict(adict[1])
    return sorted_dict(sorteddoubledict)

def list_from_double_dict(doubledict):
    thelist = []
    for dictvalues in list(doubledict.values()):
        for subdictvalue in list(dictvalues.values()):
            thelist.append(subdictvalue)
    return thelist

# digs through a dict of dicts of dicts (and so on) recursively using the given keys.
# returns None if a key isn't valid.
def digForData(data, keys):
    try:
        try:
            return digForData(data[keys[0]], keys[1:])
        except IndexError:
            return data[keys[0]]
    except KeyError:
        return None


# data sorters.

def speciesAlphaSorted(species):
    return sorted_dict(species)

def speciesAlphaSortedList(species):
    return list(speciesAlphaSorted(species).values())

def speciesDexSorted(species):
    return dict(sorted(species.items(), key = lambda item: item[1].dex))

def speciesDexSortedList(species):
    return list(speciesDexSorted(species).values())

def setsAlphaSorted(sets):
    return sorted_double_dict(sets)

def setsAlphaSortedList(sets):
    return list_from_double_dict(setsAlphaSorted(sets))

def setsDexSorted(sets):
    sorteddoubledict = {}
    for adict in sets.items():
        sorteddoubledict[adict[0]] = sorted_dict(adict[1])
    return dict(sorted(sorteddoubledict.items(), key = lambda subdict: subdict[1][list(subdict[1].keys())[0]].species.dex))

def setsDexSortedList(sets):
    return list_from_double_dict(setsDexSorted(sets))

def trainersAlphaSorted(trainers):
    return sorted_double_dict(trainers)

def trainersAlphaSortedList(trainers):
    return list_from_double_dict(trainersAlphaSorted(trainers))


# derived data.

def allMoves(sets):
    allMoves = set()
    for aset in sets:
        for move in aset.moves:
            allMoves.add(move)
    return sorted(allMoves)

def allItems(sets):
    allItems = set()
    for aset in sets:
        allItems.add(aset.item)
    return sorted(allItems)

# returns a triple dict of {BattleNum.value} to {tclass} to {tname} to Trainer.
# trainers that appear in more than one BattleNum will appear multiple times.
def battlenumToTrainers(trainers):
    bTT = {}
    bTT["All"] = trainersAlphaSorted(trainers)
    for battlenum in list(core.BattleNum):
        bTT[battlenum.value] = {}
        for trainer in trainersAlphaSortedList(trainers):
            if battlenum in trainer.battlenums:
                if trainer.tclass not in bTT[battlenum.value].keys():
                    bTT[battlenum.value][trainer.tclass] = {}
                bTT[battlenum.value][trainer.tclass][trainer.tname] = trainer
    return bTT

# returns a dict of {tclass} to "{tname1}, {tname2}, ..." to SetProvider.
# the purpose is to group together trainers with identical iv, battlenums, and sets. which is quite common.
def groupedSetProviders(trainers):
    gSP = {}
    for trainer in trainersAlphaSortedList(trainers):
        if trainer.tclass not in gSP.keys():
            gSP[trainer.tclass] = {}
            gSP[trainer.tclass][trainer.tname] = trainer.asSetProvider()
        else:
            for entry in gSP[trainer.tclass].items():
                if entry[1].isIdenticalProvider(trainer):
                    gSP[trainer.tclass].pop(entry[0])
                    gSP[trainer.tclass][entry[0] + ", " + trainer.tname] = trainer.asSetProvider()
                    break
            else: # what the fuck
                gSP[trainer.tclass][trainer.tname] = trainer.asSetProvider()
    return gSP

# the unholy combination
def battlenumToGroupedSetProviders(trainers):
    gSP = groupedSetProviders(trainers)
    bTGSP = {}
    bTGSP["All"] = gSP
    for battlenum in list(core.BattleNum):
        bTGSP[battlenum.value] = {}
        for gSPentry in gSP.items():
            for gSPsubentry in gSPentry[1].items():
                if battlenum in gSPsubentry[1].battlenums:
                    if gSPentry[0] not in bTGSP[battlenum.value].keys():
                        bTGSP[battlenum.value][gSPentry[0]] = {}
                    bTGSP[battlenum.value][gSPentry[0]][gSPsubentry[0]] = gSPsubentry[1]
    return bTGSP

