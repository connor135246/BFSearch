# core


from enum import Enum, IntEnum
import math


# a pokemon species.

class Type(IntEnum):
    Normal = 0
    Fighting = 1
    Flying = 2
    Poison = 3
    Ground = 4
    Rock = 5
    Bug = 6
    Ghost = 7
    Steel = 8
    Fire = 9
    Water = 10
    Grass = 11
    Electric = 12
    Psychic = 13
    Ice = 14
    Dragon = 15
    Dark = 16

class Species(object):
    # dex - a number, name - a string, types - a Type list of length 1 or 2, baseSpeed - a positive number, abilities - a string list of length 1 or 2
    def __init__(self, dex, name, types, baseSpeed, abilities):
        self.dex = dex
        self.name = name
        self.types = types
        self.baseSpeed = baseSpeed
        self.abilities = abilities

    def __str__(self):
        return f"{self.name} (#{self.dex})"

    def hasOneAbility(self):
        return len(self.abilities) == 1

    def hasType(self, atype):
        return atype in self.types


# a pokemon set.

class Stat(IntEnum):
    HP = 0
    Atk = 1
    Def = 2
    SpA = 3
    SpD = 4
    Spe = 5

class Nature(Enum):
    Hardy = (Stat.Atk, Stat.Atk)
    Lonely = (Stat.Atk, Stat.Def)
    Brave = (Stat.Atk, Stat.Spe)
    Adamant = (Stat.Atk, Stat.SpA)
    Naughty = (Stat.Atk, Stat.SpD)
    Bold = (Stat.Def, Stat.Atk)
    Docile = (Stat.Def, Stat.Def)
    Relaxed = (Stat.Def, Stat.Spe)
    Impish = (Stat.Def, Stat.SpA)
    Lax = (Stat.Def, Stat.SpD)
    Timid = (Stat.Spe, Stat.Atk)
    Hasty = (Stat.Spe, Stat.Def)
    Serious = (Stat.Spe, Stat.Spe)
    Jolly = (Stat.Spe, Stat.SpA)
    Naive = (Stat.Spe, Stat.SpD)
    Modest = (Stat.SpA, Stat.Atk)
    Mild = (Stat.SpA, Stat.Def)
    Quiet = (Stat.SpA, Stat.Spe)
    Bashful = (Stat.SpA, Stat.SpA)
    Rash = (Stat.SpA, Stat.SpD)
    Calm = (Stat.SpD, Stat.Atk)
    Gentle = (Stat.SpD, Stat.Def)
    Sassy = (Stat.SpD, Stat.Spe)
    Careful = (Stat.SpD, Stat.SpA)
    Quirky = (Stat.SpD, Stat.SpD)

    def modForStat(self, stat):
        mod = 1.0
        if stat == self.value[0]:
            mod += 0.1
        if stat == self.value[1]:
            mod -= 0.1
        return mod

class EVStats(object):
    # evs - a list of Stat
    def __init__(self, evs):
        self.evs = evs
        if len(self.evs) == 2:
            self.num = 255
        elif len(self.evs) == 3:
            self.num = 170
        else:
            self.num = 0

    def getEVs(self, stat):
        if stat in self.evs:
            return self.num
        else:
            return 0

    def getShowdownEVs(self):
        result = ""
        first = True
        for stat in list(Stat):
            if stat in self.evs:
                if not first:
                    result += " / "
                result += str(self.num) + " " + stat.name
                first = False
        return result

def calculateHP(base, iv, evs, level):
    return math.floor( ( ( 2 * base + iv + math.floor( evs / 4 ) ) * level ) / 100 ) + 10 + level

def calculateNonHP(base, iv, evs, level, natureMod):
    return math.floor( ( math.floor( ( ( 2 * base + iv + math.floor( evs / 4 ) ) * level ) / 100 ) + 5 ) * natureMod )

def calculateStat(stat, base, iv, evs, level, nature):
    if stat == Stat.HP:
        return calculateHP(base, iv, evs, level)
    else:
        return calculateNonHP(base, iv, evs, level, nature.modForStat(stat))

# set group is a useful way of grouping sets together.
class SetGroup(Enum):
    # very weak pokemon with only 1 possible set
    A1 = ('A', 1, range(1, 151))
    # somewhat weak pokemon with 2 possible sets
    B1 = ('B', 1, range(151, 251))
    B2 = ('B', 2, range(251, 351))
    # pokemon with 4 possible sets
    C1 = ('C', 1, range(351, 487))
    C2 = ('C', 2, range(487, 623))
    C3 = ('C', 3, range(623, 759))
    C4 = ('C', 4, range(759, 895))
    # legendaries with 4 possible sets
    D1 = ('D', 1, range(895, 909))
    D2 = ('D', 2, range(909, 923))
    D3 = ('D', 3, range(923, 937))
    D4 = ('D', 4, range(937, 951))
    # the set number indicates which set number this is for the pokemon.

    def fullname(self):
        return self.name

    def group(self):
        return self.value[0]
    def setNumber(self):
        return self.value[1]

    # for reference
    def defaultIDRange(self):
        return self.value[2]

# hall set group is a useful way of grouping battle hall sets together.
# group is determined by bst.
class HallSetGroup(Enum):
    sub339 = ("339-", range(1, 6), range(1, 155))
    from340to439 = ("340 - 439", range(3, 9), range(155, 271))
    from440to499 = ("440 - 499", range(6, 11), range(271, 376))
    plus500 = ("500+", range(9, 11), range(376, 478))

    def fullname(self):
        return self.value[0]

    def ranks(self):
        return self.value[1]
    def appearsInRank(self, rank):
        return rank in self.ranks()

    # for reference
    def defaultIDRange(self):
        return self.value[2]

    def fromFullName(value):
        for hallsetgroup in list(HallSetGroup):
            if value == hallsetgroup.fullname():
                return hallsetgroup
        raise ValueError(f"Unknown hall set group '{value}'")

# base class of pokeset
class PokeSetBase(object):
    # species - a Species, nature - a Nature, item - a string, moves - a string list length 1 to 4, evstats - a EVStats
    def __init__(self, species, nature, item, moves, evstats):
        self.species = species
        self.nature = nature
        self.item = item
        self.moves = moves
        self.evstats = evstats

    def __str__(self):
        return self.species.name

    def getShowdownNickname(self, iv):
        if iv == 31:
            return str(self)
        else:
            return f"{self} w/ {iv} IVs"

    def getShowdownFormat(self, iv, abilitySlot = -1, level = 50, hideItem = False):
        string = f"{self.getShowdownNickname(iv)} ({self.species.name})"
        if not hideItem:
            string += f" @ {self.item}"
        string += "  \n"
        if abilitySlot == -1:
            if self.species.hasOneAbility():
                string += f"Ability: {self.species.abilities[0]}  \n"
        else:
            string += f"Ability: {self.species.abilities[abilitySlot]}  \n"
        if level != 100:
            string += f"Level: {level}  \n"
        string += f"EVs: {self.evstats.getShowdownEVs()}  \n"
        string += f"{self.nature.name} Nature  \n"
        if iv != 31:
            string += f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe  \n"
        for move in self.moves:
            string += f"- {move}  \n"
        return string

    def getSpeed(self, iv, level = 50):
        return calculateStat(Stat.Spe, self.species.baseSpeed, iv, self.evstats.getEVs(Stat.Spe), level, self.nature)

# your average pokeset
class PokeSet(PokeSetBase):
    # sid - a number, setgroup - a SetGroup, species - a Species, pset - a number, nature - a Nature, item - a string, moves - a string list length 1 to 4, evstats - a EVStats
    def __init__(self, sid, setgroup, species, pset, nature, item, moves, evstats):
        PokeSetBase.__init__(self, species, nature, item, moves, evstats)
        self.sid = sid
        self.setgroup = setgroup
        self.pset = pset

    def __str__(self):
        return f"{self.species.name} {self.pset}"

# pokeset in the battle hall
class HallPokeSet(PokeSetBase):
    # hid - a number, hallsetgroup - a HallSetGroup, species - a Species, nature - a Nature, item - a string, moves - a string list length 1 to 4, evstats - a EVStats
    def __init__(self, hid, hallsetgroup, species, nature, item, moves, evstats):
        PokeSetBase.__init__(self, species, nature, item, moves, evstats)
        self.hid = hid
        self.hallsetgroup = hallsetgroup

    def __str__(self):
        return f"{self.species.name} (Hall)"

# a trainer.

class BattleNum(Enum):
    s1 = "1 - 6"
    e1 = "7"
    s2 = "8 - 13"
    e2 = "14"
    s3 = "15 - 20"
    e3 = "21"
    s4 = "22 - 27"
    e4 = "28"
    s5 = "29 - 34"
    e5 = "35"
    s6 = "36 - 41"
    e6 = "42"
    s7 = "43 - 48"
    e7 = "49"
    s99 = "50+"

    def fromNumber(num):
        try:
            return BattleNum(str(num))
        except ValueError:
            if num in range(1, 7):
                return BattleNum.s1
            elif num in range(8, 14):
                return BattleNum.s2
            elif num in range(15, 21):
                return BattleNum.s3
            elif num in range(22, 28):
                return BattleNum.s4
            elif num in range(29, 35):
                return BattleNum.s5
            elif num in range(36, 42):
                return BattleNum.s6
            elif num in range(43, 49):
                return BattleNum.s7
            elif num > 49:
                return BattleNum.s99
            else:
                raise ValueError(f"Unknown battle range '{num}'")

    def isEnder(self):
        return self == BattleNum.e1 or self == BattleNum.e2 or self == BattleNum.e3 or self == BattleNum.e4 or self == BattleNum.e5 or self == BattleNum.e6 or self == BattleNum.e7 or self.isBeyond()

    def isBeyond(self):
        return self == BattleNum.s99

    def toEnder(self):
        if self.isEnder():
            return self
        else:
            return list(BattleNum)[list(BattleNum).index(self) + 1]

    def isBrainBattle(self):
        return self == BattleNum.e3 or self == BattleNum.e7

# a facility and its rules.
# it's here next to the trainer class, but facilities aren't really a property of trainers. they're used at a higher level.
# it seemed unnecessary to have 3 identical copies of all 300 trainers for the 3 facilities that are identical for my purposes.
# if it becomes useful to do so, it would probably become a property of SetProvider.
class Facility(Enum):
    # normal facilities - Any_Normal represents all 3
    Tower = 0
    Arcade = 1
    Castle = 2
    Any_Normal = 3
    # factory
    Factory_50 = 4
    Factory_Open = 5
    # hall is not necessary - trainer doesn't matter in hall

    def level(self):
        return 100 if self == Facility.Factory_Open else 50
    def hideItem(self):
        return self == Facility.Arcade or self == Facility.Castle

    def isNormal(self):
        return self == Facility.Tower or self == Facility.Arcade or self == Facility.Castle or self == Facility.Any_Normal
    def isFactory(self):
        return self == Facility.Factory_50 or self == Facility.Factory_Open

# base class of trainer that doesn't have tid, tclass, or tname.
class SetProvider(object):
    # minIV - a number, maxIV - a number, battlenums - a list of BattleNum, sets - a dictionary of '{name}' to dictionary of '{pset}' to PokeSet
    def __init__(self, minIV, maxIV, battlenums, sets):
        self.minIV = minIV
        self.maxIV = maxIV
        self.battlenums = battlenums
        self.sets = sets
        '''
        self.setgroups = []
        for pname, nextDict in self.sets.items():
            for pset, pokeset in nextDict.items():
                self.setgroups.append(pokeset.setgroup)
        '''

    def isIdenticalProvider(self, other):
        return self.minIV == other.minIV and self.maxIV == other.maxIV and self.battlenums == other.battlenums and self.sets == other.sets

class Trainer(SetProvider):
    # tid - a number, iv - a number, tclass - a string, tname - a string, battlenums - a list of BattleNum, sets - a dictionary of '{name}' to dictionary of '{pset}' to PokeSet, facility - a Facility
    def __init__(self, tid, iv, tclass, tname, battlenums, sets, facility):
        SetProvider.__init__(self, iv, iv, battlenums, sets)
        self.tid = tid
        self.iv = iv
        self.tclass = tclass
        self.tname = tname
        # you shouldn't use this at all.
        self._facility = facility

    def __str__(self):
        return f"{self.tclass} {self.tname}"

    def asSetProvider(self):
        return SetProvider(self.iv, self.iv, self.battlenums, self.sets)


# a pokemon set owned by a trainer.

# base class of TrainersPokeSet that just has a pokeset and an iv
class PokeSetWithIV(object):
    # pokeset - a PokeSet, iv - a number
    def __init__(self, pokeset, iv):
        self.pokeset = pokeset
        self.iv = iv

    def __str__(self):
        return self.getShowdownNickname()

    def getShowdownNickname(self):
        return self.pokeset.getShowdownNickname(self.iv)

    def getShowdownFormat(self, abilitySlot = -1, level = 50, hideItem = False):
        return self.pokeset.getShowdownFormat(self.iv, abilitySlot = abilitySlot, level = level, hideItem = hideItem)

    def getSpeed(self, level = 50):
        return self.pokeset.getSpeed(self.iv, level = level)

    def isIdenticalSet(self, other):
        return self.pokeset == other.pokeset and self.iv == other.iv

class TrainersPokeSet(PokeSetWithIV):
    # trainer - a Trainer, pokeset - a PokeSet
    def __init__(self, trainer, pokeset):
        PokeSetWithIV.__init__(self, pokeset, trainer.iv)
        self.trainer = trainer

    def __str__(self):
        return f"{str(self.trainer)}'s {str(self.pokeset)}"

    def asPokeSetWithIV(self):
        return PokeSetWithIV(self.pokeset, self.iv)
