# data


import logging
from operator import itemgetter, attrgetter
from collections import defaultdict

from bfsearch import core, parsing


# data container.

class DataHolder(object):
    def __init__(self):
        # true if it has no data!
        self.isEmpty = True

        # dictionary of {name} to Species
        self.species = {}
        # dictionary of {name} to dictionary of {pset} to PokeSet
        self.sets = {}
        # dictionary of {name} to HallPokeSet
        self.hall_sets = {}
        # dictionary of {Facility} to dictionary of {tclass} to dictionary of {tname} to Trainer
        self.facilities = {}

    # tries to build data! returns error message.
    def fillerup(self):
        try:
            self.species, self.sets, self.facilities, self.hall_sets = parsing.buildData()
            self.isEmpty = False
            logging.info("Parsed data!")
            return ""
        except parsing.DataException as e:
            self.species, self.sets, self.facilities, self.hall_sets = {}, {}, {}, {}
            self.isEmpty = True
            logging.warning(e, exc_info = True)
            return e.__class__.__name__ + " - " + str(e)


# general methods.

def sorted_dict(adict):
    return defaultdict(ndict, sorted(adict.items(), key = itemgetter(0)))

def sorted_double_dict(doubledict):
    sorteddoubledict = ndict()
    for key, nextDict in doubledict.items():
        sorteddoubledict[key] = sorted_dict(nextDict)
    return sorted_dict(sorteddoubledict)

def list_from_double_dict(doubledict):
    thelist = []
    for dictvalues in list(doubledict.values()):
        for subdictvalue in list(dictvalues.values()):
            thelist.append(subdictvalue)
    return thelist

# empty or generic key in a dict
emptyKey = "---"

# wow! an auto-nesting dictionary!
def ndict():
    return defaultdict(ndict)


# data sorters.

def speciesAlphaSorted(species):
    return sorted_dict(species)

def speciesAlphaSortedList(species):
    return list(speciesAlphaSorted(species).values())

def speciesDexSorted(species):
    return defaultdict(ndict, sorted(species.items(), key = lambda item: attrgetter("dex", "name")(item[1])))

def speciesDexSortedList(species):
    return list(speciesDexSorted(species).values())

def setsAlphaSorted(sets):
    return sorted_double_dict(sets)

def setsAlphaSortedList(sets):
    return list_from_double_dict(setsAlphaSorted(sets))

def setsDexSorted(sets):
    sorteddoubledict = ndict()
    for key, nextDict in sets.items():
        sorteddoubledict[key] = sorted_dict(nextDict)
    return defaultdict(ndict, sorted(sorteddoubledict.items(), key = lambda subdict: attrgetter("species.dex", "species.name")(list(subdict[1].values())[0])))

def setsDexSortedList(sets):
    return list_from_double_dict(setsDexSorted(sets))

def trainersAlphaSorted(trainers):
    return sorted_double_dict(trainers)

def trainersAlphaSortedList(trainers):
    return list_from_double_dict(trainersAlphaSorted(trainers))

def hallSetsAlphaSorted(hall_sets):
    return sorted_dict(hall_sets)

def hallSetsAlphaSortedList(hall_sets):
    return list(hallSetsAlphaSorted(hall_sets).values())

def hallSetsDexSorted(hall_sets):
    return defaultdict(ndict, sorted(hall_sets.items(), key = lambda item: attrgetter("species.dex", "species.name")(item[1])))

def hallSetsDexSortedList(hall_sets):
    return list(hallSetsDexSorted(hall_sets).values())


# derived data.

def allPokemonAlpha(sets):
    return setsAlphaSorted(sets).keys()

def allPokemonDex(sets):
    return setsDexSorted(sets).keys()

def allMoves(sets):
    allMoves = set()
    for aset in setsAlphaSortedList(sets):
        for move in aset.moves:
            allMoves.add(move)
    return sorted(allMoves)

def allItems(sets):
    return sorted({aset.item for aset in setsDexSortedList(sets)})

def allTrainerClasses(trainers):
    return trainersAlphaSorted(trainers).keys()

def allTrainerNames(trainers):
    return sorted({trainer.tname for trainer in trainersAlphaSortedList(trainers)})

# returns a dict of {tclass} to a list of possible {tnames}. no actual Trainer objects involved.
def tclassToTName(trainers):
    tTT = ndict()
    for tclass, nextDict in trainersAlphaSorted(trainers).items():
        tTT[tclass] = list(nextDict.keys())
    return tTT

def genericSetProvider(sets):
    return core.SetProvider(31, list(core.BattleNum), sets)

# returns a triple dict of {BattleNum.value} to {tclass} to {tname} to Trainer.
# trainers that appear in more than one BattleNum will appear multiple times.
def battlenumToTrainers(trainers):
    bTT = ndict()
    bTT[emptyKey] = trainersAlphaSorted(trainers)
    for battlenum in list(core.BattleNum):
        for trainer in trainersAlphaSortedList(trainers):
            if battlenum in trainer.battlenums:
                bTT[battlenum.value][trainer.tclass][trainer.tname] = trainer
    return bTT

# returns a dict of {tclass} to "{tname1}, {tname2}, ..." to SetProvider.
# the purpose is to group together trainers with identical iv, battlenums, and sets. which is quite common.
def groupedSetProviders(trainers):
    gSP = ndict()
    for trainer in trainersAlphaSortedList(trainers):
        if trainer.tclass not in gSP.keys():
            gSP[trainer.tclass][trainer.tname] = trainer.asSetProvider()
        else:
            for tnames, setProvider in gSP[trainer.tclass].items():
                if setProvider.isIdenticalProvider(trainer):
                    gSP[trainer.tclass].pop(tnames)
                    gSP[trainer.tclass][tnames + ", " + trainer.tname] = trainer.asSetProvider()
                    break
            else:  # what the fuck
                gSP[trainer.tclass][trainer.tname] = trainer.asSetProvider()
    return gSP

# the unholy combination
def battlenumToGroupedSetProviders(trainers):
    gSP = groupedSetProviders(trainers)
    bTGSP = ndict()
    bTGSP[emptyKey] = gSP
    for battlenum in list(core.BattleNum):
        for tclass, nextDict in gSP.items():
            for tnames, setProvider in nextDict.items():
                if battlenum in setProvider.battlenums:
                    bTGSP[battlenum.value][tclass][tnames] = setProvider
    return bTGSP

# returns a list of every single individual pokemon held by every trainer. there are a lot of duplicates.
# totals:
# tower/arcade/castle: 16111 + 6 (palmer) + 6 (dahlia) + 12 (darach)
# factory (50): 77880
# factory (open): 105760
def everyIndividualPokemon(trainers):
    # exclude thorton's placeholder pokemon from search
    return [core.TrainersPokeSet(trainer, aset) for tclass, nextDict in trainers.items() if tclass != 'Factory Head' for tname, trainer in nextDict.items() for aset in setsAlphaSortedList(trainer.sets)]

# returns a dict of {PokeSetWithIV} to {[Trainer,...]} from the list of TrainersPokeSet.
def groupUniquePokemon(listTrainersPokeSet):
    uniques = ndict()
    for tps in listTrainersPokeSet:
        # slight optimization: trainer data is pretty nicely ordered by default, so pswis basically get added in order.
        for pswi in reversed(uniques.keys()):
            if pswi.isIdenticalSet(tps):
                uniques[pswi].append(tps.trainer)
                break
        else:
            uniques[tps.asPokeSetWithIV()] = [tps.trainer]
    return uniques

# returns a list of every unique pokemon held by trainers. a unique pokemon is a particular set with a particular iv.
# totals:
# tower/arcade/castle: 1585
# factory (50): 1494
# factory (open): 2944
def everyUniquePokemon(trainers):
    return [pswi for pswi, _ in groupUniquePokemon(everyIndividualPokemon(trainers))]

# returns a dict of {rank} to {name} to HallPokeSet
def rankToHallSets(hall_sets):
    rTHS = ndict()
    for rank in range(1, 11):
        for name, hall_set in hall_sets.items():
            if hall_set.hallsetgroup.appearsInRank(rank):
                rTHS[rank][name] = hall_set
    return rTHS

# returns a dict of {Type} to {rank} to {name} to HallPokeSet
def typeToRankToHallSets(hall_sets):
    rTHS = rankToHallSets(hall_sets)
    tTRTHS = ndict()
    for atype in list(core.Type):
        for rank, nextDict in rTHS.items():
            for name, hall_set in nextDict.items():
                if hall_set.species.hasType(atype):
                    tTRTHS[atype.name][rank][name] = hall_set
    return tTRTHS

# returns a dict of {HallSetGroup.fullname()} to {name} to HallPokeSet
def hallSetGroupToHallSets(hall_sets):
    hSGTHS = ndict()
    for name, hall_set in hall_sets.items():
        hSGTHS[hall_set.hallsetgroup.fullname()][name] = hall_set
    return hSGTHS
