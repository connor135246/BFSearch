# browsehall


import math

from tkinter import *
from tkinter import ttk

from bfsearch import core, data
from bfsearch.tkinter import common
from bfsearch.translate import tr


# base page for single hall set browsing
# similar to browse.BrowseSetsPageBase
class BrowseHallSetsPageBase(common.SharedPageElements):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.mainBox = ttk.Labelframe(self, text = "")

        ## pokemon selector
        self.setSelect = ttk.Frame(self.mainBox, padding = (5, 5, 5, 0))
        for i in range(0, 8):
            self.setSelect.columnconfigure(i, weight = 1)
        self.setSelect.rowconfigure(0, weight = 1)

        # group combo
        self.buildGroupCombo(self.setSelect)
        self.gridGroupCombo(0, 0)
        self.groupLabel['text'] = tr("page.hall_sets.group")

        # species combo box
        self.buildPokeCombo(self.setSelect)
        self.gridPokeCombo(2, 0)

        # level spin box
        self.levelLabel = self.addSimpleLabel(self.setSelect, tr("page.hall_sets.level"), 4, 0)
        self.level = IntVar(self.setSelect, value = 50)
        self.levelBox = ttk.Spinbox(self.setSelect, from_ = 14, to = 100, textvariable = self.level, command = self.handleLevelBox, width = 5)
        self.levelBox.grid(column = 5, row = 0, sticky = (W, E), padx = 1)

        # iv spin box
        self.buildIVBox(self.setSelect)
        self.gridIVBox(6, 0)

        # sort toggle
        self.buildSortToggle(self.mainBox)

        # output & clipboard options
        self.buildOutput(self.mainBox)

        # set up initial state
        self.updateSet()

    def gridSetSelect(self, column, row):
        self.setSelect.grid(column = column, row = row, sticky = (W, N, E, S))

    def filterByGroup(self, sortedData):
        if self.group.get() == data.emptyKey:
            return sortedData
        else:
            return data.filterHallSetsByGroup(sortedData, self.group.get())

    # when the group combo box updates, tells the poke combo box to update
    def handleGroupCombo(self, event = None):
        if self.group.get() == data.emptyKey:
            self.setToolTip(self.groupCombo, tr("page.generic.tooltip.empty_key"))
        else:
            self.setToolTip(self.groupCombo, self.group.get())
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)

    def setLevelBox(self, minLevel, maxLevel):
        self.levelBox['from_'] = minLevel
        self.levelBox['to'] = maxLevel
        if minLevel == maxLevel:
            self.setToolTip(self.levelBox, tr("page.hall_calc.levelBox.tooltip.fixed"))
            self.levelBox.state(["disabled"])
        else:
            self.setToolTip(self.levelBox, tr("page.generic.range", self.levelBox['from'], self.levelBox['to']))
            self.levelBox.state(["!disabled"])
        # manually ensure the spinbox var is valid
        if self.level.get() > maxLevel:
            self.level.set(maxLevel)
        if self.level.get() < minLevel:
            self.level.set(minLevel)
        # manually notify the spinbox that it changed
        self.handleLevelBox()

    def getLevel(self):
        return self.level.get()

    def handlePokeCombo(self, event):
        self.updateSet()

    def handleLevelBox(self):
        self.updateSet()

    def updateSet(self):
        super().updateSet()
        self.currentSet = self.getSorted()[self.poke.get()]
        if self.currentSet:
            self.updateOutput()
            self.clipboardButton.state(["!disabled"])
            self.setToolTip(self.pokeCombo, str(self.currentSet.species))
        else:
            self.clearResults()

    def clearResults(self):
        self.setOutputText(tr("page.all_sets.empty_results"))
        self.clipboardButton.state(["disabled"])
        self.setToolTip(self.pokeCombo, "")


# browse all hall sets
class BrowseAllHallSetsPage(BrowseHallSetsPageBase):
    def __init__(self, parent, hallSetProvider):
        super().__init__(parent)

        # build
        self.hallSetProvider = hallSetProvider
        self.sortedAlpha = data.hallSetsAlphaSorted(self.hallSetProvider.hall_sets)
        self.sortedDex = data.hallSetsDexSorted(self.hallSetProvider.hall_sets)

        # place the main box
        self.gridSortToggle(0, 0)
        self.gridSetSelect(0, 1)
        self.gridOutput(0, 2)
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(2, weight = 1)

        # place this tab
        infoLabel = self.buildSimpleLabel(self, tr("page.hall_sets.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        # initial state
        self.fillGroupCombo([hallsetgroup.fullname() for hallsetgroup in self.hallSetProvider.hallsetgroups])
        if "Weavile" in self.getSorted().keys():
            self.poke.set("Weavile")
            self.updateSet()
        self.setIVBox([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 31])
        self.setLevelBox(14, 100)


# browse hall sets by type and rank, plus argenta
class CalcHallSetsPage(BrowseHallSetsPageBase):
    def __init__(self, parent, typeToRankToHallSets, hallSetGroupToHallSets):
        super().__init__(parent)

        self.HALL_BRAIN_SILVER = tr("page.hall_calc.brain_silver")
        self.HALL_BRAIN_GOLD = tr("page.hall_calc.brain_gold")

        # build
        self.typeToRankToHallSets = typeToRankToHallSets
        self.hallSetGroupToHallSets = hallSetGroupToHallSets

        # remove group combo
        self.groupLabel.grid_forget()
        self.groupCombo.grid_forget()
        self.setSelect.columnconfigure(0, weight = 0)
        self.setSelect.columnconfigure(1, weight = 0)

        # place the main box
        ## your pokemon's info
        pokeInfo = ttk.Frame(self.mainBox, padding = (5, 0, 5, 5))
        for i in range(0, 4):
            pokeInfo.columnconfigure(i, weight = 1)
        pokeInfo.rowconfigure(0, weight = 1)

        # your level spin box
        self.yourLevelLabel = self.addSimpleLabel(pokeInfo, tr("page.hall_calc.your_level"), 0, 0)
        self.yourLevel = IntVar(pokeInfo, value = 50)
        self.yourLevelBox = ttk.Spinbox(pokeInfo, from_ = 30, to = 100, textvariable = self.yourLevel, command = self.handleYourLevelBox, width = 5)
        self.yourLevelBox.grid(column = 1, row = 0, sticky = (W, E), padx = 1)

        # your bst combo box
        self.yourBSTLabel = self.addSimpleLabel(pokeInfo, tr("page.hall_calc.your_bst"), 2, 0, tooltip = tr("page.hall_calc.your_bst.tooltip"))
        self.yourBST = StringVar(pokeInfo)
        self.yourBSTCombo = self.addSimpleCombobox(self.yourBST, self.handleYourBSTCombo, pokeInfo, 3, 0)

        ## battle selector
        battleSelect = ttk.Frame(self.mainBox, padding = (5, 0, 5, 5))
        for i in range(0, 6):
            battleSelect.columnconfigure(i, weight = 1)
        battleSelect.rowconfigure(0, weight = 1)

        # type combo box
        self.typeLabel = self.addSimpleLabel(battleSelect, tr("page.hall_calc.type"), 0, 0, tooltip = tr("page.hall_calc.type.tooltip"))
        self.type = StringVar(battleSelect)
        self.typeCombo = self.addSimpleCombobox(self.type, self.handleTypeCombo, battleSelect, 1, 0)

        # rank spin box
        self.rankLabel = self.addSimpleLabel(battleSelect, tr("page.hall_calc.rank"), 2, 0)
        self.rank = IntVar(battleSelect, value = 1)
        self.rankBox = ttk.Spinbox(battleSelect, from_ = 1, to = 10, textvariable = self.rank, command = self.handleRankBox, width = 5)
        self.rankBox.grid(column = 3, row = 0, sticky = (W, E), padx = 1)

        # visited types spin box
        self.visitedTypesLabel = self.addSimpleLabel(battleSelect, tr("page.hall_calc.visited_types"), 4, 0, tooltip = tr("page.hall_calc.visited_types.tooltip"))
        self.visitedTypes = IntVar(battleSelect, value = 0)
        self.visitedTypesBox = ttk.Spinbox(battleSelect, from_ = 0, to = 17, textvariable = self.visitedTypes, command = self.handleVisitedTypesBox, width = 5)
        self.visitedTypesBox.grid(column = 5, row = 0, sticky = (W, E), padx = 1)

        pokeInfo.grid(column = 0, row = 0, sticky = (W, N, E, S))
        battleSelect.grid(column = 0, row = 1, sticky = (W, N, E, S))
        self.gridSortToggle(0, 2)
        self.gridSetSelect(0, 3)
        self.gridOutput(0, 4)
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(4, weight = 1)

        # place this tab

        infoLabel = self.buildSimpleLabel(self, tr("page.hall_calc.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.setToolTip(self.yourLevelBox, tr("page.generic.range", self.yourLevelBox['from'], self.yourLevelBox['to']))
        self.setToolTip(self.rankBox, tr("page.generic.range", self.rankBox['from'], self.rankBox['to']))
        self.setToolTip(self.visitedTypesBox, tr("page.generic.range", self.visitedTypesBox['from'], self.visitedTypesBox['to']))

        # initial state

        self.fillCombobox(self.yourBSTCombo, [hallsetgroup.fullname() for hallsetgroup in core.HallSetGroup], self.yourBST)
        self.yourBSTCombo.current(3)
        self.setToolTip(self.yourBSTCombo, self.yourBST.get())

        typeValues = list(self.tTRTHS().keys())
        typeValues.append(self.HALL_BRAIN_SILVER)
        typeValues.append(self.HALL_BRAIN_GOLD)
        self.fillCombobox(self.typeCombo, typeValues, self.type)

    # for checking by type/rank
    def tTRTHS(self):
        return self.typeToRankToHallSets

    # for checking frontier brain
    def hSGTHS(self):
        return self.hallSetGroupToHallSets

    def checkingBrain(self):
        return self.type.get() == self.HALL_BRAIN_SILVER or self.type.get() == self.HALL_BRAIN_GOLD

    # when the your bst combo box updates, if type is a hall brain, updates the poke combo box
    def handleYourBSTCombo(self, event):
        self.setToolTip(self.yourBSTCombo, self.yourBST.get())
        if self.checkingBrain():
            self.updateCalcSets()

    # when the your level box updates, updates opp level
    def handleYourLevelBox(self):
        self.updateCalcLevel()

    # when the type combo box updates, tells the poke combo box to update
    def handleTypeCombo(self, event):
        # brain doesn't have rank
        if self.checkingBrain():
            self.rankBox.state(["disabled"])
        else:
            self.rankBox.state(["!disabled"])
        self.updateCalcSets()

    # when the rank box updates, tells the poke combo box to update
    def handleRankBox(self):
        self.updateCalcSets()

    # when the visited types box updates, updates opp level
    def handleVisitedTypesBox(self):
        self.updateCalcLevel()

    def updateCalcLevel(self):
        if self.checkingBrain():
            oppLevel = self.yourLevel.get()
        else:
            oppLevel = calcOppLevel(self.yourLevel.get(), self.rank.get(), self.visitedTypes.get())
        self.setLevelBox(oppLevel, oppLevel)

    def updateCalcIV(self):
        if self.checkingBrain():
            iv = 31
        else:
            iv = ivFromRank(self.rank.get())
        self.setIVBox([iv])

    def updateCalcSets(self):
        if self.type.get() == self.HALL_BRAIN_GOLD:
            currentHallSets = self.hSGTHS()[core.HallSetGroup.plus500.fullname()]
        elif self.type.get() == self.HALL_BRAIN_SILVER:
            currentHallSets = self.hSGTHS()[self.yourBST.get()]
        else:
            currentHallSets = self.tTRTHS()[self.type.get()][self.rank.get()]
        if currentHallSets:
            self.sortedAlpha = data.hallSetsAlphaSorted(currentHallSets)
            self.sortedDex = data.hallSetsDexSorted(currentHallSets)
            # when the type/rank/brain selection updates, tells the poke combo box to update
            self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)
            self.updateCalcLevel()
            self.updateCalcIV()
            self.setToolTip(self.typeCombo, self.type.get())
        else:
            self.clearCalcSetsResults()

    def clearCalcSetsResults(self):
        self.fillComboboxKeys(self.pokeCombo, {}, self.poke)
        self.setToolTip(self.typeCombo, "")

def ivFromRank(rank):
    # start at 8 and go up 2 per rank up to 26
    return 6 + rank * 2

def calcOppLevel(playerLevel, rank, visitedTypes):
    # visitedTypes is the number of types that been been visited before and are therefore above rank 1.
    # but we want to know the number of types that are above rank 1 other than this one.
    numberOfTypesAboveRank1ExcludingThisOne = None
    # if we're checking a rank above 1, then the "number of types above rank 1" count includes the current rank, which it shouldn't, so we subtract 1.
    if rank > 1:
        numberOfTypesAboveRank1ExcludingThisOne = max(visitedTypes - 1, 0)
    # if we're checking rank 1, then the "number of types above rank 1" count already does not include the current rank.
    else:
        numberOfTypesAboveRank1ExcludingThisOne = visitedTypes

    baseLevel = playerLevel - 3 * math.sqrt(playerLevel)
    incrementPerRank = math.sqrt(playerLevel) / 5
    maxLevel = math.ceil( baseLevel + numberOfTypesAboveRank1ExcludingThisOne / 2 + ( rank - 1 ) * incrementPerRank )
    return min(playerLevel, maxLevel)
