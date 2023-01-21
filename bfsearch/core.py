# core


from enum import Enum
from enum import IntEnum
import math


# a pokemon species.

class Species(object):
    # dex - a number, name - a string, baseSpeed - a positive number, abilities - a string list of length 1 or 2
    def __init__(self, dex, name, baseSpeed, abilities):
        self.dex = dex
        self.name = name
        self.baseSpeed = baseSpeed
        self.abilities = abilities

    def __str__(self):
        return f"{self.name} (#{self.dex})"

    def hasOneAbility(self):
        return len(self.abilities) == 1


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
        for ev in self.evs:
            if not first:
                result += " / "
            result += str(self.num) + " " + ev.name
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

class PokeSet(object):
    # sid - a number, species - a Species, pset - a number, nature - a Nature, item - a string, moves - a string list length 1 to 4, evstats - a EVStats
    def __init__(self, sid, species, pset, nature, item, moves, evstats):
        self.sid = sid
        self.species = species
        self.pset = pset
        self.nature = nature
        self.item = item
        self.moves = moves
        self.evstats = evstats

    def __str__(self):
        return f"{self.species.name} {self.pset}"

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
            if num in range(1,7):
                return s1
            elif num in range(8,14):
                return s2
            elif num in range(15,21):
                return s3
            elif num in range(22,28):
                return s4
            elif num in range(29,35):
                return s5
            elif num in range(36,42):
                return s6
            elif num in range(43,49):
                return s7
            elif num > 49:
                return s99
            else:
                raise Exception("Unknown battle range!")

    def isEnder(self):
        return self == e1 or self == e2 or self == e3 or self == e4 or self == e5 or self == e6 or self == e7 or self.isBeyond()

    def isBeyond(self):
        return self == s99

    def toEnder(self):
        if isEnder(self):
            return self
        else:
            return list(BattleNum)[list(BattleNum).index(self) + 1]

    def isBrainBattle(self):
        return self == e3 or self == e7

# base class of trainer that doesn't have tid, tclass, or tname.
class SetProvider(object):
    # minIV - a number, maxIV - a number, battlenums - a list of BattleNum, sets - a dictionary of '{name}' to dictionary of '{pset}' to PokeSet
    def __init__(self, minIV, maxIV, battlenums, sets):
        self.minIV = minIV
        self.maxIV = maxIV
        self.battlenums = battlenums
        self.sets = sets

    def isIdenticalProvider(self, other):
        return self.minIV == other.minIV and self.maxIV == other.maxIV and self.battlenums == other.battlenums and self.sets == other.sets

class Trainer(SetProvider):
    # tid - a number, iv - a number, tclass - a string, tname - a string, battlenums - a list of BattleNum, sets - a dictionary of '{name}' to dictionary of '{pset}' to PokeSet
    def __init__(self, tid, iv, tclass, tname, battlenums, sets):
        SetProvider.__init__(self, iv, iv, battlenums, sets)
        self.tid = tid
        self.iv = iv
        self.tclass = tclass
        self.tname = tname

    def __str__(self):
        return f"{self.tclass} {self.tname}"

    def asSetProvider(self):
        return SetProvider(self.iv, self.iv, self.battlenums, self.sets)

'''
# a pokemon set owned by a trainer.

class TrainersPokeSet(object):
    # pokeset - a PokeSet, trainer - a Trainer
    def __init__(self, pokeset, trainer):
        self.pokeset = pokeset
        self.trainer = trainer

    def __str__(self):
        return f"{self.trainer.name()}'s {self.pokeset.name()}"

    def getShowdownNickname(self):
        return self.pokeset.getShowdownNickname(self.trainer.iv)

    def getShowdownFormat(self, abilitySlot = -1, level = 50, hideItem = False):
        return self.pokeset.getShowdownFormat(self.trainer.iv, abilitySlot = abilitySlot, level = level, hideItem = hideItem)

    def getSpeed(self, level = 50):
        return self.pokeset.getSpeed(self.trainer.iv, level = level)
'''

