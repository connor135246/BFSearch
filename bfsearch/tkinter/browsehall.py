# browsehall


import math

from tkinter import *
from tkinter import ttk

from bfsearch import core, data
from bfsearch.tkinter import browse
from bfsearch.translate import tr


# base page for single hall set browsing
# similar to browse.BrowseSetsPageBase
class BrowseHallSetsPageBase(browse.SharedPageElements):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.mainBox = ttk.Labelframe(self, text = "")

        ## pokemon selector
        self.setSelect = ttk.Frame(self.mainBox, padding = (5, 5, 5, 0))
        for i in range(0, 6):
            self.setSelect.columnconfigure(i, weight = 1)
        self.setSelect.rowconfigure(0, weight = 1)

        # species combo box
        self.pokeLabel = self.addSimpleLabel(self.setSelect, tr("page.generic.pokemon"), 0, 0)
        self.poke = StringVar(self.setSelect)
        self.pokeCombo = self.addSimpleCombobox(self.poke, self.handlePokeCombo, self.setSelect, 1, 0)

        # level spin box
        self.levelLabel = self.addSimpleLabel(self.setSelect, tr("page.hall_sets.level"), 2, 0)
        self.level = IntVar(self.setSelect, value = 50)
        self.levelBox = ttk.Spinbox(self.setSelect, from_ = 14, to = 100, textvariable = self.level, command = self.handleLevelBox)
        self.levelBox.grid(column = 3, row = 0, sticky = (W, E), padx = 1)

        # iv spin box
        self.buildIVBox(self.setSelect)
        self.gridIVBox(4, 0)

        # sort toggle
        self.buildSortToggle(self.mainBox)

        # output & clipboard options
        self.buildOutput(self.mainBox)

        # set up initial state
        self.updateSet()

    def gridSetSelect(self, column, row):
        self.setSelect.grid(column = column, row = row, sticky = (W, N, E, S))

    def toggleSorting(self):
        super().toggleSorting()
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
        self.sortedAlpha = data.hallSetsAlphaSorted(self.hallSetProvider.sets)
        self.sortedDex = data.hallSetsDexSorted(self.hallSetProvider.sets)

        # place the main box
        self.gridSortToggle(0, 0)
        self.gridSetSelect(0, 1)
        self.gridOutput(0, 2)
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(2, weight = 1)

        # place this tab
        infoLabel = ttk.Label(self, text = tr("page.hall_sets.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        # initial state
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)
        if "Weavile" in self.getSorted().keys():
            self.poke.set("Weavile")
            self.updateSet()
        self.setIVBox([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 31])
        self.setLevelBox(14, 100)


# browse hall sets by type and rank, plus argenta
class CalcHallSetsPage(BrowseHallSetsPageBase):

    HALL_BRAIN_SILVER = "Hall Matron Argenta (Silver Print)"
    HALL_BRAIN_GOLD = "Hall Matron Argenta (Gold Print)"

    def __init__(self, parent, typeToRankToHallSets, hallSetGroupToHallSets):
        super().__init__(parent)

        # build
        self.typeToRankToHallSets = typeToRankToHallSets
        self.hallSetGroupToHallSets = hallSetGroupToHallSets

        # place the main box
        ## your pokemon's info
        pokeInfo = ttk.Frame(self.mainBox, padding = (5, 0, 5, 5))
        for i in range(0, 4):
            pokeInfo.columnconfigure(i, weight = 1)
        pokeInfo.rowconfigure(0, weight = 1)

        # your level spin box
        self.yourLevelLabel = self.addSimpleLabel(pokeInfo, tr("page.hall_calc.your_level"), 0, 0)
        self.yourLevel = IntVar(pokeInfo, value = 50)
        self.yourLevelBox = ttk.Spinbox(pokeInfo, from_ = 30, to = 100, textvariable = self.yourLevel, command = self.handleYourLevelBox)
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
        self.rankBox = ttk.Spinbox(battleSelect, from_ = 1, to = 10, textvariable = self.rank, command = self.handleRankBox)
        self.rankBox.grid(column = 3, row = 0, sticky = (W, E), padx = 1)

        # visited types spin box
        self.visitedTypesLabel = self.addSimpleLabel(battleSelect, tr("page.hall_calc.visited_types"), 4, 0)
        self.visitedTypes = IntVar(battleSelect, value = 0)
        self.visitedTypesBox = ttk.Spinbox(battleSelect, from_ = 0, to = 17, textvariable = self.visitedTypes, command = self.handleVisitedTypesBox)
        self.visitedTypesBox.grid(column = 5, row = 0, sticky = (W, E), padx = 1)

        pokeInfo.grid(column = 0, row = 0, sticky = (W, N, E, S))
        battleSelect.grid(column = 0, row = 1, sticky = (W, N, E, S))
        self.gridSortToggle(0, 2)
        self.gridSetSelect(0, 3)
        self.gridOutput(0, 4)
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(4, weight = 1)

        # place this tab

        infoLabel = ttk.Label(self, text = tr("page.hall_calc.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.setToolTip(self.yourLevelBox, tr("page.generic.range", self.yourLevelBox['from'], self.yourLevelBox['to']))
        self.setToolTip(self.rankBox, tr("page.generic.range", self.rankBox['from'], self.rankBox['to']))
        self.setToolTip(self.visitedTypesBox, tr("page.generic.range", self.visitedTypesBox['from'], self.visitedTypesBox['to']))

        # initial state

        yourBSTValues = []
        for hallsetgroup in list(core.HallSetGroup):
            yourBSTValues.append(hallsetgroup.fullname())
        self.fillCombobox(self.yourBSTCombo, yourBSTValues, self.yourBST)
        self.yourBSTCombo.current(3)
        self.setToolTip(self.yourBSTCombo, self.yourBST.get())

        typeValues = []
        for key in self.tTRTHS().keys():
            typeValues.append(key)
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
        if self.checkingBrain():
            self.updateCalcSets()
        # even if we don't updateCalcSets, we still want to update this tooltip
        self.setToolTip(self.yourBSTCombo, self.yourBST.get())

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
        self.setToolTip(self.yourBSTCombo, "")

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
