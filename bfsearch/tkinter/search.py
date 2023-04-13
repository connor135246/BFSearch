# search


from enum import Enum
from operator import attrgetter
from collections import defaultdict

from tkinter import *
from tkinter import ttk

from bfsearch import core, data
from bfsearch.data import ndict
from bfsearch.tkinter import browse, dialogs
from bfsearch.translate import tr


# todo: fix the searchBox changing size when you click the pokeCombo sortToggle
class SearchPage(browse.SharedPageElements):
    def __init__(self, parent, the_data):
        super().__init__(parent)

        self.data = the_data

        ## search box
        self.searchBox = ttk.Labelframe(self, text = tr("page.search.searchBox"))
        self.searchBox.columnconfigure(0, weight = 1)
        for i in range(0, 18):
            self.searchBox.rowconfigure(i, weight = 1)

        # battle number
        self.addSimpleLabel(self.searchBox, tr("page.generic.battle_number"), 0, 0)
        self.battlenum = StringVar(self.searchBox)
        self.battlenumCombo = self.addSearchCombobox(self.battlenum, self.searchBox, [battlenum.value for battlenum in list(core.BattleNum)], 0, 1)

        # trainer class and name
        # this is the only one that updates as you select it. tclass links to possible tnames.
        self.addSimpleLabel(self.searchBox, tr("page.generic.trainer"), 0, 2)
        self.tclass = StringVar(self.searchBox)
        self.tclassCombo = self.addSimpleCombobox(self.tclass, self.handleTClassCombo, self.searchBox, 0, 3, padx = 5)
        self.tname = StringVar(self.searchBox)
        self.tnameCombo = self.addSimpleCombobox(self.tname, self.searchChanged, self.searchBox, 0, 4, padx = 5)

        # pokemon
        self.addSimpleLabel(self.searchBox, tr("page.generic.pokemon"), 0, 5)
        self.sortedAlpha = data.allPokemonAlpha(self.data.sets)
        self.sortedDex = data.allPokemonDex(self.data.sets)
        self.buildSortToggle(self.searchBox)
        self.gridSortToggle(0, 6)
        self.poke = StringVar(self.searchBox)
        self.pokeCombo = self.addSearchCombobox(self.poke, self.searchBox, self.getSorted(), 0, 7)

        # held item
        self.addSimpleLabel(self.searchBox, tr("page.search.item"), 0, 8)
        self.item = StringVar(self.searchBox)
        self.itemCombo = self.addSearchCombobox(self.item, self.searchBox, data.allItems(self.data.sets), 0, 9)

        # moves
        self.addSimpleLabel(self.searchBox, tr("page.search.moves"), 0, 10)
        self.move1 = StringVar(self.searchBox)
        self.moveCombo1 = self.addSearchCombobox(self.move1, self.searchBox, data.allMoves(self.data.sets), 0, 11)
        self.move2 = StringVar(self.searchBox)
        self.moveCombo2 = self.addSearchCombobox(self.move2, self.searchBox, data.allMoves(self.data.sets), 0, 12)
        self.move3 = StringVar(self.searchBox)
        self.moveCombo3 = self.addSearchCombobox(self.move3, self.searchBox, data.allMoves(self.data.sets), 0, 13)
        self.move4 = StringVar(self.searchBox)
        self.moveCombo4 = self.addSearchCombobox(self.move4, self.searchBox, data.allMoves(self.data.sets), 0, 14)

        # search!
        separator = ttk.Separator(self.searchBox, orient = 'horizontal')
        separator.grid(column = 0, row = 15, sticky = (W, E), padx = 10, pady = 10)
        self.searchButton = ttk.Button(self.searchBox, text = tr("page.search.searchButton"), command = self.search)
        self.searchButton.grid(column = 0, row = 16, sticky = (W, E), padx = 5)
        self.clearSearchButton = ttk.Button(self.searchBox, text = tr("page.search.clearSearchButton"), command = self.clearSearch)
        self.clearSearchButton.grid(column = 0, row = 17, sticky = (W, E), padx = 5, pady = 5)

        ## results box
        self.resultsBox = ttk.Labelframe(self, text = tr("page.search.resultsBox"))
        self.resultsBox.columnconfigure(0, weight = 1)
        self.resultsBox.rowconfigure(3, weight = 1)

        # results info
        self.resultsInfo = ttk.Label(self.resultsBox, text = tr("page.search.resultsBox.default"))
        self.resultsInfo.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5)

        # results sorting
        # alphabetically organized results
        self.currentResultsA = []
        # dex number organized results
        self.currentResultsD = []
        # sort toggle button
        self.resultSortToggle = ttk.Button(self.resultsBox, command = self.toggleResultSorting)
        self.resultsAlpha = True
        self.setResultsToggleText()
        self.setToolTip(self.resultSortToggle, tr("page.search.sortToggle.tooltip"))
        self.resultSortToggle.grid(column = 0, row = 1, sticky = (W, E), padx = 5, pady = 5)

        # results combo
        self.result = StringVar(self.resultsBox)
        self.resultsCombo = self.addSimpleCombobox(self.result, self.handleResultsCombo, self.resultsBox, 0, 2, padx = 5)

        # output & clipboard options
        self.buildOutput(self.resultsBox)
        self.gridOutput(0, 3)
        self.currentIV = 31

        # trainer output
        self.trainerInfo = ttk.Label(self.resultsBox)
        self.trainerInfo.grid(column = 0, row = 5, sticky = (W, N, E, S), padx = 5)
        # view and scrollbar contained in a frame
        self.trainerViewFrame = ttk.Frame(self.resultsBox)
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

        # place this tab
        infoLabel = ttk.Label(self, text = tr("page.search.info"))
        infoLabel.grid(column = 0, row = 0, columnspan = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        facilityBox = ttk.Labelframe(self)
        facilityBox.columnconfigure(0, weight = 1)
        facilityBox.rowconfigure(0, weight = 1)
        self.buildFacility(facilityBox)
        self.gridFacility(0, 0)
        facilityBox.grid(column = 0, row = 1, columnspan = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.searchBox.grid(column = 0, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.resultsBox.grid(column = 1, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)

    # adds a search combobox connected to searchChanged
    def addSearchCombobox(self, var, parent, contents, column, row):
        # must fill before binding command, otherwise it causes problems
        combo = self.addSimpleCombobox(var, None, parent, column, row, padx = 5)
        self.fillComboboxPlusEmpty(combo, contents, var)
        combo.bind('<<ComboboxSelected>>', self.searchChanged)
        return combo

    # sets the combo box to the contents, plus an empty entry at the start
    def fillComboboxPlusEmpty(self, combo, contents, var):
        contents = (data.emptyKey, *contents)
        self.fillCombobox(combo, contents, var)

    def prepFacility(self):
        self.trainerDict = ndict()
        self.trainerDict[data.emptyKey] = data.allTrainerNames(self.data.facilities[self.facility])
        self.trainerDict.update(data.tclassToTName(self.data.facilities[self.facility]))
        self.fillComboboxKeys(self.tclassCombo, self.trainerDict, self.tclass)
        self.updateSet()
        self.searchButton['text'] = tr("page.search.searchButton")
        self.trainerInfo['text'] = tr("page.search.resultsBox.default")
        self.resultsCombo.state(["disabled"])

    # when the facility selection changes, tells everything to update
    def handleFacility(self):
        self.currentResultsA = ndict()
        self.currentResultsD = ndict()
        self.fillCombobox(self.resultsCombo, tuple(), self.result)
        self.prepFacility()
        self.resultsInfo['text'] = tr("page.search.resultsBox.default")
        self.setOutputText("")

    def toggleSorting(self):
        super().toggleSorting()
        no_selection = self.poke.get() == data.emptyKey
        self.fillComboboxPlusEmpty(self.pokeCombo, self.getSorted(), self.poke)
        if no_selection:
            # undo the search button text being marked as changed if it didn't change
            self.searchButton['text'] = tr("page.search.searchButton")

    def toggleResultSorting(self):
        self.resultsAlpha = not self.resultsAlpha
        self.setResultsToggleText()
        self.fillResultsCombo()

    def setResultsToggleText(self):
        if self.resultsAlpha:
            self.resultSortToggle['text'] = tr("page.search.sortToggle.alpha")
        else:
            self.resultSortToggle['text'] = tr("page.search.sortToggle.dex")

    def getResults(self):
        return self.currentResultsA if self.resultsAlpha else self.currentResultsD

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self, event):
        self.searchChanged(event)
        tnameData = self.trainerDict[self.tclass.get()]
        self.fillComboboxPlusEmpty(self.tnameCombo, tnameData, self.tname)

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

    def handleResultsCombo(self, event):
        self.updateSet()

    def getIV(self):
        return self.currentIV

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
        self.clipboardButton.state(["disabled"])
        self.setToolTip(self.resultsCombo, "")
        self.fillTrainerView([])
        self.trainerInfo['text'] = tr("page.search.resultsBox.trainerInfo.plural", 0)

    def searchChanged(self, event):
        self.searchButton['text'] = tr("page.search.searchButton.changed")

    def clearSearch(self):
        self.battlenumCombo.current(0)
        self.tclassCombo.current(0)
        # manually generate the combobox selected event
        self.tclassCombo.event_generate("<<ComboboxSelected>>")
        self.tnameCombo.current(0)
        self.pokeCombo.current(0)
        self.itemCombo.current(0)
        self.moveCombo1.current(0)
        self.moveCombo2.current(0)
        self.moveCombo3.current(0)
        self.moveCombo4.current(0)
        self.searchButton['text'] = tr("page.search.searchButton")

    def search(self):
        # clicking search with no selection can cause the program to hang - especially for battle factory.
        # so first ask if you're sure.
        for combo in [self.battlenumCombo, self.tclassCombo, self.tnameCombo, self.pokeCombo, self.itemCombo, self.moveCombo1, self.moveCombo2, self.moveCombo3, self.moveCombo4]:
            if combo.current() != 0:
                break
        else:  # what the fuck
            suredialog = dialogs.InfoDialog(self._root(), tr("page.search.name"), [tr("toolbar.button.ok"), tr("toolbar.button.cancel")], tr("page.search.searchButton.sure"), "gui/search.png")
            pressed = suredialog.show()
            if pressed != 0:
                return

        # grouping of combobox var, reducer, and nice name
        class SearchOption(Enum):
            BattleNum = (self.battlenum, self.reduceBattleNum, "Battle Number")
            TClass = (self.tclass, self.reduceTClass, "Trainer Class")
            TName = (self.tname, self.reduceTName, "Trainer Name")
            Species = (self.poke, self.reducePoke, "Pokemon")
            Item = (self.item, self.reduceItem, "Item")
            Move1 = (self.move1, self.reduceMove1, "Move")
            Move2 = (self.move2, self.reduceMove2, "Move")
            Move3 = (self.move3, self.reduceMove3, "Move")
            Move4 = (self.move4, self.reduceMove4, "Move")

            def var(self):
                return self.value[0]
            def reducer(self):
                return self.value[1]
            def nicename(self):
                return self.value[2]

        the_list = data.everyIndividualPokemon(self.data.facilities[self.facility])
        searchByStage = [(None, len(the_list) > 0, the_list)]
        if not searchByStage[-1][1]:
            self.emptyResults(searchByStage)
        else:
            # each searchByStage tuple is: (this SearchOption, boolean of whether this SearchOption was checked, the remaining items after this SearchOption)
            for searchoption in list(SearchOption):
                searchByStage = self.checkAndReduce(searchoption, searchByStage)
                if len(searchByStage[-1][2]) < 1:
                    self.emptyResults(searchByStage)
                    break

        searchResults = searchByStage[-1][2]
        currentResults = data.groupUniquePokemon(searchResults)
        for pswi, trainers in currentResults.items():
            currentResults[pswi] = sorted(trainers, key = str)
        # alphabetical sort
        # sort by iv - putting 31 first
        self.currentResultsA = defaultdict(ndict, sorted(currentResults.items(), key = lambda unique: -1 if unique[0].iv == 31 else unique[0].iv))
        # sort by name, then set number
        self.currentResultsA = defaultdict(ndict, sorted(self.currentResultsA.items(), key = lambda unique: attrgetter('pokeset.species.name', 'pokeset.pset')(unique[0])))
        # dex sort
        # sort by iv - putting 31 first
        self.currentResultsD = defaultdict(ndict, sorted(currentResults.items(), key = lambda unique: -1 if unique[0].iv == 31 else unique[0].iv))
        # sort by dex, then form, then set number
        self.currentResultsD = defaultdict(ndict, sorted(self.currentResultsD.items(), key = lambda unique: attrgetter('pokeset.species.dex', 'pokeset.species.name', 'pokeset.pset')(unique[0])))
        self.fillResultsCombo()

        self.resultsInfo['text'] = tr("page.search.resultsBox.done", len(searchResults), len(currentResults))
        self.searchButton['text'] = tr("page.search.searchButton")

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
        self.setOutputText(string)

    def reduceBattleNum(self, search_list):
        try:
            battlenum = core.BattleNum(self.battlenum.get())
            return [tps for tps in search_list if battlenum in tps.trainer.battlenums]
        except ValueError:
            return search_list

    def reduceTClass(self, search_list):
        return [tps for tps in search_list if self.tclass.get() == tps.trainer.tclass]

    def reduceTName(self, search_list):
        return [tps for tps in search_list if self.tname.get() == tps.trainer.tname]

    def reducePoke(self, search_list):
        return [tps for tps in search_list if self.poke.get() == tps.pokeset.species.name]

    def reduceItem(self, search_list):
        return [tps for tps in search_list if self.item.get() == tps.pokeset.item]

    def reduceMove1(self, search_list):
        return [tps for tps in search_list if self.move1.get() in tps.pokeset.moves]
    def reduceMove2(self, search_list):
        return [tps for tps in search_list if self.move2.get() in tps.pokeset.moves]
    def reduceMove3(self, search_list):
        return [tps for tps in search_list if self.move3.get() in tps.pokeset.moves]
    def reduceMove4(self, search_list):
        return [tps for tps in search_list if self.move4.get() in tps.pokeset.moves]