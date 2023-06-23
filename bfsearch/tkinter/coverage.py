# coverage


from enum import Enum
from operator import attrgetter
from collections import defaultdict

from tkinter import *
from tkinter import ttk

from bfsearch import core, data
from bfsearch.data import ndict
from bfsearch.tkinter import common, dialogs, browsehall
from bfsearch.tkinter.search import SortMode
from bfsearch.translate import tr


# player's ability
class AbilityMode(Enum):
    Any = 0
    MoldBreaker = 1
    Scrappy = 2

# coverage calculator page
# very similar to a search page
class CoveragePageBase(common.SharedPageElements):
    def __init__(self, parent, the_data):
        super().__init__(parent)
        self.data = the_data

    # makes the coverage box + calc buttons - uses 3 rows
    def buildCoverageBox(self, row):
        ## coverage box
        self.coverageBox = ttk.Labelframe(self, text = tr("page.coverage.coverageBox"))
        self.coverageBox.columnconfigure(0, weight = 1)
        for i in range(0, row + 3):
            self.coverageBox.rowconfigure(i, weight = 1)
        # calc!
        separator = ttk.Separator(self.coverageBox, orient = 'horizontal')
        separator.grid(column = 0, row = row, sticky = (W, E), padx = 10, pady = 10)
        self.calcButton = ttk.Button(self.coverageBox, text = tr("page.coverage.calcButton"), command = self.calc)
        self.calcButton.state(["disabled"])
        self.calcButton.grid(column = 0, row = row + 1, sticky = (W, E), padx = 5)
        self.clearCalcButton = ttk.Button(self.coverageBox, text = tr("page.coverage.clearCalcButton"), command = self.clearCalc)
        self.clearCalcButton.grid(column = 0, row = row + 2, sticky = (W, E), padx = 5, pady = 5)

    # makes the type and ability selectors - uses 7 rows
    def buildCoverageSelect(self, row):
        # move types
        self.addSimpleLabel(self.coverageBox, tr("page.coverage.move_types"), 0, row)
        types = [atype.name for atype in core.Type]
        self.type1 = StringVar(self.coverageBox)
        self.typeCombo1 = self.addCalcCombobox(self.type1, self.coverageBox, types, 0, row + 1)
        self.type2 = StringVar(self.coverageBox)
        self.typeCombo2 = self.addCalcCombobox(self.type2, self.coverageBox, types, 0, row + 2)
        self.type3 = StringVar(self.coverageBox)
        self.typeCombo3 = self.addCalcCombobox(self.type3, self.coverageBox, types, 0, row + 3)
        self.type4 = StringVar(self.coverageBox)
        self.typeCombo4 = self.addCalcCombobox(self.type4, self.coverageBox, types, 0, row + 4)
        # ability
        self.addSimpleLabel(self.coverageBox, tr("page.coverage.ability"), 0, row + 5)
        self.ability = StringVar(self.coverageBox)
        self.abilityCombo = self.addCalcCombobox(self.ability, self.coverageBox, ["Mold Breaker", "Scrappy"], 0, row + 6)

    # makes the results notebook
    def buildResultsNotebook(self, clazz):
        ## results pages
        # results pages share a sort
        self.resultsSort = SortMode.Alpha
        # make results pages
        self.resultsNotebook = ttk.Notebook(self)
        self.resultsNotebook.enable_traversal()
        self.zeroPage = clazz(self.resultsNotebook, self)
        self.quarterPage = clazz(self.resultsNotebook, self)
        self.halfPage = clazz(self.resultsNotebook, self)
        self.normalPage = clazz(self.resultsNotebook, self)
        self.doublePage = clazz(self.resultsNotebook, self)
        self.quadPage = clazz(self.resultsNotebook, self)
        self.resultsPages = [self.zeroPage, self.quarterPage, self.halfPage, self.normalPage, self.doublePage, self.quadPage]
        for page in self.resultsPages:
            self.resultsNotebook.add(page)

    # adds a calc combobox connected to calcChanged
    def addCalcCombobox(self, var, parent, contents, column, row):
        # must fill before binding command, otherwise it causes problems
        combo = self.addSimpleCombobox(var, None, parent, column, row, padx = 5)
        self.fillComboboxPlusEmpty(combo, contents, var)
        combo.bind('<<ComboboxSelected>>', self.calcChanged)
        return combo

    def prepFacility(self):
        self.resultsNotebook.tab(0, text = tr("page.coverage.zeroPage.default"))
        self.resultsNotebook.tab(1, text = tr("page.coverage.quarterPage.default"))
        self.resultsNotebook.tab(2, text = tr("page.coverage.halfPage.default"))
        self.resultsNotebook.tab(3, text = tr("page.coverage.normalPage.default"))
        self.resultsNotebook.tab(4, text = tr("page.coverage.doublePage.default"))
        self.resultsNotebook.tab(5, text = tr("page.coverage.quadPage.default"))

    # when the facility selection changes, tells everything to update
    def handleFacility(self):
        self.calcButton['text'] = tr("page.coverage.calcButton")
        self.prepFacility()
        for page in self.resultsPages:
            page.handleFacility()

    # results pages share a sort
    def toggleResultSorting(self):
        self.resultsSort = self.resultsSort.next()
        for page in self.resultsPages:
            page.setResultsToggleText()
            page.fillResultsCombo()

    def calcChanged(self, event):
        self.calcButton['text'] = tr("page.coverage.calcButton.changed")
        if self.typeCombo1.current() == 0 and self.typeCombo2.current() == 0 and self.typeCombo3.current() == 0 and self.typeCombo4.current() == 0:
            self.calcButton.state(["disabled"])
        else:
            self.calcButton.state(["!disabled"])

    ### override and call super last to add functionality
    def clearCalc(self):
        self.typeCombo1.current(0)
        self.typeCombo2.current(0)
        self.typeCombo3.current(0)
        self.typeCombo4.current(0)
        self.abilityCombo.current(0)
        self.calcButton['text'] = tr("page.coverage.calcButton")
        self.calcButton.state(["disabled"])

    def getAttackingTypes(self):
        return [core.Type[varval] for varval in [self.type1.get(), self.type2.get(), self.type3.get(), self.type4.get()] if self.shouldCheck(varval)]

    ### override to add functionality
    def calc(self):
        pass

    # the_list is data. searchoptions is an iterable of things that have .var(), .reducer(), and .nicename().
    def doSearchByStage(self, the_list, searchoptions):
        self.emptyResultsString = None
        searchByStage = [(None, len(the_list) > 0, the_list)]
        if not searchByStage[-1][1]:
            self.emptyResults(searchByStage)
        else:
            # each searchByStage tuple is: (this SearchOption, boolean of whether this SearchOption was checked, the remaining items after this SearchOption)
            for searchoption in searchoptions:
                searchByStage = self.checkAndReduce(searchoption, searchByStage)
                if len(searchByStage[-1][2]) < 1:
                    self.emptyResults(searchByStage)
                    break
        return searchByStage

    def checkAndReduce(self, searchoption, searchByStage):
        previousResult = searchByStage[-1][2]
        this_check = len(previousResult) > 0 and self.shouldCheck(searchoption.var().get())
        if this_check:
            this_result = searchoption.reducer()(previousResult)
        else:
            this_result = previousResult
        return searchByStage + [(searchoption, this_check, this_result)]

    def shouldCheck(self, value):
        return value != '' and value != data.emptyKey

    def emptyResults(self, searchByStage):
        string = tr("page.search.result.none") + "\n\n"
        count = 1
        for searchoption, check, result in searchByStage:
            if searchoption is None:
                string += tr("page.search.result.initial", len(result)) + "\n"
                if not check:
                    string += "  "*count + "-> " + tr("page.search.result.initial.none") + "\n"
                    count += 1
            elif check:
                string += "  "*count + "-> " + tr("page.search.result.option", len(result), searchoption.nicename(), searchoption.var().get()) + "\n"
                count += 1
        self.emptyResultsString = string


# each tab in the results
# very similar to a search page's results box
class ResultsTabPageBase(common.SharedPageElements):
    def __init__(self, parent, parentpage):
        super().__init__(parent)

        self.parentpage = parentpage

    def buildResultsBox(self, outputOffset = 0):
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(3 + outputOffset, weight = 1)
        # results info
        self.resultsInfo = self.buildSimpleLabel(self, tr("page.search.resultsBox.default"))
        self.resultsInfo.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5)
        # results sorting
        # alphabetically organized results
        self.currentResultsA = ndict()
        # dex number organized results
        self.currentResultsD = ndict()
        # speed organized results
        self.currentResultsS = ndict()
        # sort toggle button
        self.resultSortToggle = ttk.Button(self, command = self.toggleResultSorting)
        self.setResultsToggleText()
        self.setToolTip(self.resultSortToggle, tr("page.search.sortToggle.tooltip"))
        self.resultSortToggle.grid(column = 0, row = 1, sticky = (W, E), padx = 5, pady = 5)
        # results combo
        self.result = StringVar(self)
        self.resultsCombo = self.addSimpleCombobox(self.result, self.handleResultsCombo, self, 0, 2, padx = 5)
        # output & clipboard options
        self.buildOutput(self)
        self.gridOutput(0, 3 + outputOffset)
        self.currentIV = 31

    # results pages share a sort
    def toggleResultSorting(self):
        self.parentpage.toggleResultSorting()

    def setResultsToggleText(self):
        if self.parentpage.resultsSort == SortMode.Speed:
            self.resultSortToggle['text'] = tr("page.search.sortToggle.speed")
        elif self.parentpage.resultsSort == SortMode.Dex:
            self.resultSortToggle['text'] = tr("page.search.sortToggle.dex")
        else:
            self.resultSortToggle['text'] = tr("page.search.sortToggle.alpha")

    def getResults(self):
        if self.parentpage.resultsSort == SortMode.Speed:
            return self.currentResultsS
        elif self.parentpage.resultsSort == SortMode.Dex:
            return self.currentResultsD
        else:
            return self.currentResultsA

    ### override to add functionality
    def fillResultsCombo(self):
        pass

    def handleResultsCombo(self, event):
        self.updateSet()

    def getIV(self):
        return self.currentIV

    # check parent page's facility
    def getHideItem(self):
        return self.parentpage.facility.hideItem()

    # check parent page's facility
    def getLevel(self):
        return self.parentpage.facility.level()


# coverage page for normal sets
class CoveragePage(CoveragePageBase):
    def __init__(self, parent, the_data):
        super().__init__(parent, the_data)

        self.buildCoverageBox(9)

        # battle number
        self.addSimpleLabel(self.coverageBox, tr("page.generic.battle_number"), 0, 0)
        self.battlenum = StringVar(self.coverageBox)
        self.battlenumCombo = self.addCalcCombobox(self.battlenum, self.coverageBox, [battlenum.value for battlenum in core.BattleNum], 0, 1)

        self.buildCoverageSelect(2)

        self.buildResultsNotebook(ResultsTabPage)

        # set up initial state
        self.prepFacility()

        # place this tab
        infoLabel = self.buildSimpleLabel(self, tr("page.coverage.info"))
        infoLabel.grid(column = 0, row = 0, columnspan = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        facilityBox = ttk.Labelframe(self)
        facilityBox.columnconfigure(0, weight = 1)
        facilityBox.rowconfigure(0, weight = 1)
        self.buildFacility(facilityBox)
        self.gridFacility(0, 0)
        facilityBox.grid(column = 0, row = 1, columnspan = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.coverageBox.grid(column = 0, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.resultsNotebook.grid(column = 1, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)

    def clearCalc(self):
        self.battlenumCombo.current(0)
        super().clearCalc()

    def calc(self):
        # clicking calc with no selection can cause the program to hang - especially for battle factory.
        # so first ask if you're sure.
        if self.battlenumCombo.current() == 0:
            suredialog = dialogs.InfoDialog(self._root(), tr("page.coverage.name"), [tr("toolbar.button.ok"), tr("toolbar.button.cancel")], tr("page.coverage.calcButton.sure"), "gui/coverage.png")
            pressed = suredialog.show()
            if pressed != 0:
                return

        # grouping of combobox var, reducer, and nice name
        class SearchOption(Enum):
            BattleNum = (self.battlenum, self.reduceBattleNum, "Battle Number")

            def var(self):
                return self.value[0]
            def reducer(self):
                return self.value[1]
            def nicename(self):
                return self.value[2]

        searchByStage = self.doSearchByStage(data.everyIndividualPokemon(self.data.facilities[self.facility]), SearchOption)

        searchResults = searchByStage[-1][2]
        currentResults = data.groupUniquePokemon(searchResults)

        tabresults = []
        for _ in range(6): # 6 pages
            tabresults.append([ndict(), 0]) # results and counter
        attackingTypes = self.getAttackingTypes()
        abilitymode = AbilityMode(self.abilityCombo.current())
        for pswi, trainers in currentResults.items():
            final_multiplier = getFinalMultiplier(attackingTypes, pswi.pokeset.species.types, abilitymode, pswi.pokeset.species.abilities)
            fm_index = getFinalMultiplierIndex(final_multiplier)
            tabresults[fm_index][0][pswi] = trainers
            tabresults[fm_index][1] += len(trainers)

        self.zeroPage.applyCurrentResults(tabresults[0][0], tabresults[0][1])
        self.quarterPage.applyCurrentResults(tabresults[1][0], tabresults[1][1])
        self.halfPage.applyCurrentResults(tabresults[2][0], tabresults[2][1])
        self.normalPage.applyCurrentResults(tabresults[3][0], tabresults[3][1])
        self.doublePage.applyCurrentResults(tabresults[4][0], tabresults[4][1])
        self.quadPage.applyCurrentResults(tabresults[5][0], tabresults[5][1])

        if len(searchResults) > 0:
            def getPercent(count):
                return f"{round(count / len(searchResults) * 100)}%"
            self.resultsNotebook.tab(0, text = tr("page.coverage.zeroPage.count", tabresults[0][1], getPercent(tabresults[0][1])))
            self.resultsNotebook.tab(1, text = tr("page.coverage.quarterPage.count", tabresults[1][1], getPercent(tabresults[1][1])))
            self.resultsNotebook.tab(2, text = tr("page.coverage.halfPage.count", tabresults[2][1], getPercent(tabresults[2][1])))
            self.resultsNotebook.tab(3, text = tr("page.coverage.normalPage.count", tabresults[3][1], getPercent(tabresults[3][1])))
            self.resultsNotebook.tab(4, text = tr("page.coverage.doublePage.count", tabresults[4][1], getPercent(tabresults[4][1])))
            self.resultsNotebook.tab(5, text = tr("page.coverage.quadPage.count", tabresults[5][1], getPercent(tabresults[5][1])))
        else:
            self.prepFacility()
            if self.emptyResultsString:
                for page in self.resultsPages:
                    page.setOutputText(self.emptyResultsString)

        self.calcButton['text'] = tr("page.coverage.calcButton")

    def reduceBattleNum(self, search_list):
        try:
            battlenum = core.BattleNum(self.battlenum.get())
            return [tps for tps in search_list if battlenum in tps.trainer.battlenums]
        except ValueError:
            return search_list

# results tab for normal sets
class ResultsTabPage(ResultsTabPageBase):
    def __init__(self, parent, parentpage):
        super().__init__(parent, parentpage)

        self.buildResultsBox()

        # trainer output
        self.trainerInfo = self.buildSimpleLabel(self, "")
        self.trainerInfo.grid(column = 0, row = 5, sticky = (W, N, E, S), padx = 5)
        # view and scrollbar contained in a frame
        self.trainerViewFrame = ttk.Frame(self)
        self.trainerViewFrame.columnconfigure(0, weight = 1)
        self.trainerViewFrame.rowconfigure(0, weight = 1)
        self.trainerView = ttk.Treeview(self.trainerViewFrame, height = 5, show = 'tree')
        trainerViewScrollbar = ttk.Scrollbar(self.trainerViewFrame, orient = 'vertical', command = self.trainerView.yview)
        self.trainerView['yscrollcommand'] = trainerViewScrollbar.set
        self.trainerView.grid(column = 0, row = 0, sticky = (W, N, E, S), pady = 5)
        trainerViewScrollbar.grid(column = 1, row = 0, sticky = (W, N, E, S), pady = 5)
        self.trainerViewFrame.grid(column = 0, row = 6, sticky = (W, N, E, S), padx= 5)

        # set up initial state
        self.prepFacility()

    def prepFacility(self):
        self.updateSet()
        self.trainerInfo['text'] = tr("page.search.resultsBox.default")
        self.resultsCombo.state(["disabled"])

    # when the facility selection changes, tells everything to update
    def handleFacility(self):
        self.currentResultsA = ndict()
        self.currentResultsD = ndict()
        self.currentResultsS = ndict()
        self.fillCombobox(self.resultsCombo, tuple(), self.result)
        self.prepFacility()
        self.resultsInfo['text'] = tr("page.search.resultsBox.default")
        self.setOutputText("")

    def fillResultsCombo(self):
        self.fillCombobox(self.resultsCombo, [pswi.getShowdownNickname() for pswi in self.getResults().keys()], self.result)

    def fillTrainerView(self, trainers):
        self.trainerView.delete(*self.trainerView.get_children())
        for trainer in trainers:
            self.trainerView.insert('', 'end', text = str(trainer))
        if len(trainers) == 1:
            self.trainerInfo['text'] = tr("page.search.resultsBox.trainerInfo.singular", len(trainers))
        else:
            self.trainerInfo['text'] = tr("page.search.resultsBox.trainerInfo.plural", len(trainers))

    def updateSet(self):
        super().updateSet()
        if len(self.resultsCombo['values']) > 0 and self.resultsCombo.current() < len(self.getResults()):
            pswi, trainers = list(self.getResults().items())[self.resultsCombo.current()]
            self.currentSet = pswi.pokeset
            self.currentIV = pswi.iv
            self.updateOutput()
            self.fillTrainerView(trainers)
            self.clipboardButton.state(["!disabled"])
            self.setToolTip(self.resultsCombo, self.result.get())
        else:
            self.clearResults()

    def clearResults(self):
        self.setOutputText("")
        self.clipboardButton.state(["disabled"])
        self.setToolTip(self.resultsCombo, "")
        self.fillTrainerView([])
        self.trainerInfo['text'] = tr("page.search.resultsBox.trainerInfo.plural", 0)

    def applyCurrentResults(self, currentResults, currentResultsCount):
        # sort trainers
        for pswi, trainers in currentResults.items():
            currentResults[pswi] = sorted(trainers, key = str)
        # sort by iv, putting 31 first
        currentResults = defaultdict(ndict, sorted(currentResults.items(), key = lambda unique: -1 if unique[0].iv == 31 else unique[0].iv))
        # alphabetical sort - sort by name, then set number
        self.currentResultsA = defaultdict(ndict, sorted(currentResults.items(), key = lambda unique: attrgetter('pokeset.species.name', 'pokeset.pset')(unique[0])))
        # dex sort - sort by dex, then form, then set number
        self.currentResultsD = defaultdict(ndict, sorted(self.currentResultsA.items(), key = lambda unique: attrgetter('pokeset.species.dex')(unique[0])))
        # speed sort - sort by speed, then name, then set number
        self.currentResultsS = defaultdict(ndict, sorted(self.currentResultsA.items(), key = lambda unique, self = self: -unique[0].getAdjustedSpeed(hideItem = self.facility.hideItem(), level = self.facility.level())))
        self.fillResultsCombo()

        self.resultsInfo['text'] = tr("page.search.resultsBox.done", currentResultsCount, len(currentResults))


# coverage page for hall sets
class HallCoveragePage(CoveragePageBase):
    def __init__(self, parent, the_data):
        super().__init__(parent, the_data)

        self.buildCoverageBox(13)

        # type
        self.addSimpleLabel(self.coverageBox, tr("page.hall_calc.type"), 0, 0)
        self.type = StringVar(self.coverageBox)
        self.typeCombo = self.addCalcCombobox(self.type, self.coverageBox, [atype.name for atype in core.Type], 0, 1)

        # rank
        self.addSimpleLabel(self.coverageBox, tr("page.hall_calc.rank"), 0, 2)
        self.rank = StringVar(self.coverageBox)
        self.rankCombo = self.addCalcCombobox(self.rank, self.coverageBox, range(1, 11), 0, 3)
        self.rankCombo['height'] = 11

        # bst
        self.addSimpleLabel(self.coverageBox, tr("page.hall_search.bst"), 0, 4)
        self.bst = StringVar(self.coverageBox)
        self.bstCombo = self.addCalcCombobox(self.bst, self.coverageBox, [hallsetgroup.fullname() for hallsetgroup in core.HallSetGroup], 0, 5)

        self.buildCoverageSelect(6)

        # results pages share level
        self.level = IntVar(self, value = 50)
        self.buildResultsNotebook(HallResultsTabPage)

        # set up initial state
        self.prepFacility()

        # place this tab
        infoLabel = self.buildSimpleLabel(self, tr("page.hall_coverage.info"))
        infoLabel.grid(column = 0, row = 0, columnspan = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.coverageBox.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.resultsNotebook.grid(column = 1, row = 1, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(1, weight = 1)

    # results pages share level
    def handleLevelBox(self):
        for page in self.resultsPages:
            page.updateSet()
            # re-sort speed while maintaining selection
            prevResult = page.result.get()
            page.speedSort()
            page.fillResultsCombo()
            page.result.set(prevResult)
            page.resultsCombo.event_generate("<<ComboboxSelected>>")

    def clearCalc(self):
        self.typeCombo.current(0)
        self.rankCombo.current(0)
        self.bstCombo.current(0)
        super().clearCalc()

    def calc(self):

        # grouping of combobox var, reducer, and nice name
        class SearchOption(Enum):
            Type = (self.type, self.reduceType, "Type")
            Rank = (self.rank, self.reduceRank, "Rank")
            BST = (self.bst, self.reduceBST, "BST")

            def var(self):
                return self.value[0]
            def reducer(self):
                return self.value[1]
            def nicename(self):
                return self.value[2]

        searchByStage = self.doSearchByStage(data.hallSetsAlphaSortedList(self.data.hall_sets), SearchOption)

        searchResults = searchByStage[-1][2]
        iv = browsehall.ivFromRank(int(self.rank.get())) if self.rank.get().isdecimal() else 31
        # turn into pswi's
        currentResults = [core.PokeSetWithIV(hallset, iv) for hallset in searchResults]

        tabresults = []
        for _ in range(6): # 6 pages
            tabresults.append([]) # results
        attackingTypes = self.getAttackingTypes()
        abilitymode = AbilityMode(self.abilityCombo.current())
        for pswi in currentResults:
            final_multiplier = getFinalMultiplier(attackingTypes, pswi.pokeset.species.types, abilitymode, pswi.pokeset.species.abilities)
            fm_index = getFinalMultiplierIndex(final_multiplier)
            tabresults[fm_index].append(pswi)

        self.zeroPage.applyCurrentResults(tabresults[0])
        self.quarterPage.applyCurrentResults(tabresults[1])
        self.halfPage.applyCurrentResults(tabresults[2])
        self.normalPage.applyCurrentResults(tabresults[3])
        self.doublePage.applyCurrentResults(tabresults[4])
        self.quadPage.applyCurrentResults(tabresults[5])

        if len(searchResults) > 0:
            def getPercent(alist):
                return f"{round(len(alist) / len(searchResults) * 100)}%"
            self.resultsNotebook.tab(0, text = tr("page.coverage.zeroPage.count", len(tabresults[0]), getPercent(tabresults[0])))
            self.resultsNotebook.tab(1, text = tr("page.coverage.quarterPage.count", len(tabresults[1]), getPercent(tabresults[1])))
            self.resultsNotebook.tab(2, text = tr("page.coverage.halfPage.count", len(tabresults[2]), getPercent(tabresults[2])))
            self.resultsNotebook.tab(3, text = tr("page.coverage.normalPage.count", len(tabresults[3]), getPercent(tabresults[3])))
            self.resultsNotebook.tab(4, text = tr("page.coverage.doublePage.count", len(tabresults[4]), getPercent(tabresults[4])))
            self.resultsNotebook.tab(5, text = tr("page.coverage.quadPage.count", len(tabresults[5]), getPercent(tabresults[5])))
        else:
            self.prepFacility()
            if self.emptyResultsString:
                for page in self.resultsPages:
                    page.setOutputText(self.emptyResultsString)

        self.calcButton['text'] = tr("page.coverage.calcButton")

    def reduceType(self, search_list):
        try:
            thetype = core.Type[self.type.get()]
            return [hallset for hallset in search_list if hallset.species.hasType(thetype)]
        except KeyError:
            return search_list

    def reduceRank(self, search_list):
        rank = int(self.rank.get()) if self.rank.get().isdecimal() else -1
        groups = core.HallSetGroup.groupsFromRank(rank)
        if len(groups) < 1:
            return search_list
        else:
            return [hallset for hallset in search_list if hallset.hallsetgroup in groups]

    def reduceBST(self, search_list):
        try:
            bst = core.HallSetGroup.fromFullName(self.bst.get())
            return [hallset for hallset in search_list if hallset.hallsetgroup == bst]
        except ValueError:
            return search_list

# results tab for hall sets
class HallResultsTabPage(ResultsTabPageBase):
    def __init__(self, parent, parentpage):
        super().__init__(parent, parentpage)

        self.buildResultsBox(1)
        # level spin box
        levelFrame = ttk.Frame(self, padding = (5, 5, 5, 0))
        levelFrame.columnconfigure(0, weight = 1)
        levelFrame.columnconfigure(1, weight = 1)
        levelFrame.rowconfigure(0, weight = 1)
        self.levelLabel = self.addSimpleLabel(levelFrame, tr("page.hall_sets.level"), 0, 0)
        self.levelBox = ttk.Spinbox(levelFrame, from_ = 14, to = 100, textvariable = self.parentpage.level, command = self.handleLevelBox)
        self.levelBox.grid(column = 1, row = 0, sticky = (W, E), padx = 1)
        levelFrame.grid(column = 0, row = 3, sticky = (W, N, E, S))

        # set up initial state
        self.updateSet()
        self.resultsCombo.state(["disabled"])

    # results pages share level
    def getLevel(self):
        return self.parentpage.level.get()

    def handleLevelBox(self):
        self.parentpage.handleLevelBox()

    def speedSort(self):
        self.currentResultsS = sorted(self.currentResultsA, key = lambda hswi, self = self: -hswi.getAdjustedSpeed(hideItem = False, level = self.getLevel()))

    def fillResultsCombo(self):
        self.fillCombobox(self.resultsCombo, [hswi.getShowdownNickname() for hswi in self.getResults()], self.result)

    def updateSet(self):
        super().updateSet()
        if len(self.resultsCombo['values']) > 0 and self.resultsCombo.current() < len(self.getResults()):
            hswi = self.getResults()[self.resultsCombo.current()]
            self.currentSet = hswi.pokeset
            self.currentIV = hswi.iv
            self.updateOutput()
            self.clipboardButton.state(["!disabled"])
            self.setToolTip(self.resultsCombo, self.result.get())
        else:
            self.clearResults()

    def clearResults(self):
        self.setOutputText("")
        self.clipboardButton.state(["disabled"])
        self.setToolTip(self.resultsCombo, "")

    def applyCurrentResults(self, currentResults):
        # alphabetical sort - sort by name
        self.currentResultsA = sorted(currentResults, key = lambda hswi: attrgetter('pokeset.species.name')(hswi))
        # dex sort - sort by dex, then form
        self.currentResultsD = sorted(self.currentResultsA, key = lambda hswi: attrgetter('pokeset.species.dex')(hswi))
        # speed sort - sort by speed, then dex, then form
        self.speedSort()
        self.fillResultsCombo()

        self.resultsInfo['text'] = tr("page.hall_search.resultsBox.done", len(currentResults))


# which page number the final multiplier corresponds to
def getFinalMultiplierIndex(final_multiplier):
    if final_multiplier <= 0:
        return 0 # immune
    elif final_multiplier < 0.375:
        return 1 # quarter
    elif final_multiplier < 0.75:
        return 2 # half
    elif final_multiplier < 1.5:
        return 3 # normal
    elif final_multiplier < 3:
        return 4 # double
    else:
        return 5 # quad

def getFinalMultiplier(attackingTypes, defendingTypes, abilitymode, defendingAbilities):
    multipliers = []
    for attackingType in attackingTypes:
        multiplier = 1
        for defendingType in defendingTypes:
            multiplier *= multiplierFromTypeChart(attackingType, defendingType, abilitymode)
        if abilitymode != AbilityMode.MoldBreaker:
            abilityMultipliers = []
            for ability in defendingAbilities:
                if ability == "Wonder Guard":
                    abilityMultipliers.append(0 if multiplier <= 1 else multiplier)
                else:
                    abilityMultipliers.append(multiplierFromAbility(ability, attackingType))
            multiplier *= min(abilityMultipliers) # assume worst case for opponent's ability
        multipliers.append(multiplier)
    return max(multipliers) # assume player chooses the best move

from bfsearch.core import Type

def default1():
    return lambda: defaultdict(lambda: 1)

# type chart
def multiplierFromTypeChart(attackingType, defendingType, abilitymode):
    if abilitymode == AbilityMode.Scrappy and defendingType == Type.Ghost and (attackingType == Type.Normal or attackingType == Type.Fighting):
        return 1
    return typeChart[attackingType][defendingType]

typeChart = defaultdict(default1())
typeChart[Type.Normal].update({Type.Rock: 0.5, Type.Ghost: 0, Type.Steel: 0.5})
typeChart[Type.Fighting].update({Type.Normal: 2, Type.Flying: 0.5, Type.Poison: 0.5, Type.Rock: 2, Type.Bug: 0.5, Type.Ghost: 0, Type.Steel: 2, Type.Psychic: 0.5, Type.Ice: 2, Type.Dark: 2})
typeChart[Type.Flying].update({Type.Fighting: 2, Type.Rock: 0.5, Type.Bug: 2, Type.Steel: 0.5, Type.Grass: 2, Type.Electric: 0.5})
typeChart[Type.Poison].update({Type.Poison: 0.5, Type.Ground: 0.5, Type.Rock: 0.5, Type.Ghost: 0.5, Type.Steel: 0, Type.Grass: 2})
typeChart[Type.Ground].update({Type.Flying: 0, Type.Poison: 2, Type.Rock: 2, Type.Bug: 0.5, Type.Steel: 2, Type.Fire: 2, Type.Grass: 0.5, Type.Electric: 2})
typeChart[Type.Rock].update({Type.Fighting: 0.5, Type.Flying: 2, Type.Ground: 0.5, Type.Bug: 2, Type.Steel: 0.5, Type.Fire: 2, Type.Ice: 2})
typeChart[Type.Bug].update({Type.Fighting: 0.5, Type.Flying: 0.5, Type.Poison: 0.5, Type.Ghost: 0.5, Type.Steel: 0.5, Type.Fire: 0.5, Type.Grass: 2, Type.Psychic: 2, Type.Dark: 2})
typeChart[Type.Ghost].update({Type.Normal: 0, Type.Ghost: 2, Type.Steel: 0.5, Type.Psychic: 2, Type.Dark: 0.5})
typeChart[Type.Steel].update({Type.Rock: 2, Type.Steel: 0.5, Type.Fire: 0.5, Type.Water: 0.5, Type.Electric: 0.5, Type.Ice: 2})
typeChart[Type.Fire].update({Type.Rock: 0.5, Type.Bug: 2, Type.Steel: 2, Type.Fire: 0.5, Type.Water: 0.5, Type.Grass: 2, Type.Ice: 2, Type.Dragon: 0.5})
typeChart[Type.Water].update({Type.Ground: 2, Type.Rock: 2, Type.Fire: 2, Type.Water: 0.5, Type.Grass: 0.5, Type.Dragon: 0.5})
typeChart[Type.Grass].update({Type.Flying: 0.5, Type.Poison: 0.5, Type.Ground: 2, Type.Rock: 2, Type.Bug: 0.5, Type.Steel: 0.5, Type.Fire: 0.5, Type.Water: 2, Type.Grass: 0.5, Type.Dragon: 0.5})
typeChart[Type.Electric].update({Type.Flying: 2, Type.Ground: 0, Type.Water: 2, Type.Grass: 0.5, Type.Electric: 0.5, Type.Dragon: 0.5})
typeChart[Type.Psychic].update({Type.Fighting: 2, Type.Poison: 2, Type.Steel: 0.5, Type.Psychic: 0.5, Type.Dark: 0})
typeChart[Type.Ice].update({Type.Flying: 2, Type.Ground: 2, Type.Steel: 0.5, Type.Fire: 0.5, Type.Water: 0.5, Type.Grass: 2, Type.Ice: 0.5, Type.Dragon: 2})
typeChart[Type.Dragon].update({Type.Steel: 0.5, Type.Dragon: 2})
typeChart[Type.Dark].update({Type.Fighting: 0.5, Type.Ghost: 2, Type.Steel: 0.5, Type.Psychic: 2, Type.Dark: 0.5})
#.update({Type.Normal: 1, Type.Fighting: 1, Type.Flying: 1, Type.Poison: 1, Type.Ground: 1, Type.Rock: 1, Type.Bug: 1, Type.Ghost: 1, Type.Steel: 1, Type.Fire: 1, Type.Water: 1, Type.Grass: 1, Type.Electric: 1, Type.Psychic: 1, Type.Ice: 1, Type.Dragon: 1, Type.Dark: 1})

# opponent's ability
def multiplierFromAbility(ability, attackingType):
    return abilityLookup[ability][attackingType]

abilityLookup = defaultdict(default1())
abilityLookup["Levitate"].update({Type.Ground: 0})
abilityLookup["Water Absorb"].update({Type.Water: 0})
abilityLookup["Volt Absorb"].update({Type.Electric: 0})
abilityLookup["Flash Fire"].update({Type.Fire: 0})
abilityLookup["Dry Skin"].update({Type.Fire: 1.25, Type.Water: 0})
abilityLookup["Thick Fat"].update({Type.Fire: 0.5, Type.Ice: 0.5})
abilityLookup["Motor Drive"].update({Type.Electric: 0})
abilityLookup["Heatproof"].update({Type.Fire: 0.5})
