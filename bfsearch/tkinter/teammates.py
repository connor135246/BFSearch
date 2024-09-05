# teammates


from operator import attrgetter

from tkinter import *
from tkinter import ttk

from bfsearch import core, data
from bfsearch.data import ndict
from bfsearch.tkinter import common
from bfsearch.translate import tr


# teammate matching page
# somewhat similar to a search page
class TeammateMatchingPage(common.SharedPageElements):
    def __init__(self, parent, the_data):
        super().__init__(parent)
        self.data = the_data

        self['padding'] = (0, 5, 0, 5)

        ## matching box!
        self.matchBox = ttk.Labelframe(self, text = tr("page.teammate_matching.matchBox"))
        self.matchBox.columnconfigure(1, weight = 1)
        self.matchBox.columnconfigure(2, weight = 1)
        self.matchBox.columnconfigure(4, weight = 1)
        self.matchBox.columnconfigure(5, weight = 1)
        self.matchBox.rowconfigure(1, weight = 1)

        # battle number combo box
        self.battlenumLabel = self.buildSimpleLabel(self.matchBox, tr("page.generic.battle_number"))
        self.battlenumLabel.grid(column = 0, row = 0, padx = 5)
        self.battlenum = StringVar(self.matchBox)
        self.battlenumCombo = self.addSimpleCombobox(self.battlenum, None, self.matchBox, 1, 0, padx = 5)
        self.fillComboboxPlusEmpty(self.battlenumCombo, [battlenum.value for battlenum in core.BattleNum], self.battlenum)
        self.battlenumCombo.bind('<<ComboboxSelected>>', self.matchChanged)
        self.battlenumCombo['width'] = 11

        # shared sort toggle
        self.sortedAlpha = data.allPokemonAlpha(self.data.sets)
        self.sortedDex = data.allPokemonDex(self.data.sets)
        self.buildSortToggle(self.matchBox)
        self.gridSortToggle(2, 0)

        separator = ttk.Separator(self.matchBox, orient = 'vertical')
        separator.grid(column = 3, row = 0, sticky = (N, S), padx = 5, pady = 5)

        # match button
        self.matchButton = ttk.Button(self.matchBox, text = tr("page.teammate_matching.matchButton"), command = self.match)
        self.matchButton.grid(column = 4, row = 0, sticky = (W, E), padx = 5)
        self.matchButton.state(["disabled"])
        self.clearMatchButton = ttk.Button(self.matchBox, text = tr("page.teammate_matching.clearMatchButton"), command = self.clearMatch)
        self.clearMatchButton.grid(column = 5, row = 0, sticky = (W, E), padx = 5, pady = 5)

        # teammates
        self.items = data.allItems(self.data.sets)
        self.moves = data.allMoves(self.data.sets)
        teammateBoxesWrapper = ttk.Frame(self.matchBox)
        self.teammate1Box = TeammateFrame(teammateBoxesWrapper, self, 1)
        self.teammate2Box = TeammateFrame(teammateBoxesWrapper, self, 2)
        self.teammate3Box = TeammateFrame(teammateBoxesWrapper, self, 3)
        self.teammateBoxes = [self.teammate1Box, self.teammate2Box, self.teammate3Box]
        self.teammate1Box.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.teammate2Box.grid(column = 1, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.teammate3Box.grid(column = 2, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        teammateBoxesWrapper.grid(column = 0, row = 1, columnspan = 6, sticky = (W, N, E, S))
        teammateBoxesWrapper.columnconfigure(0, weight = 1)
        teammateBoxesWrapper.columnconfigure(1, weight = 1)
        teammateBoxesWrapper.columnconfigure(2, weight = 1)
        teammateBoxesWrapper.rowconfigure(0, weight = 1)

        ## results box!
        self.resultsBox = ttk.Labelframe(self, text = tr("page.teammate_matching.resultsBox"))
        self.resultsBox.columnconfigure(2, weight = 1)
        self.resultsBox.rowconfigure(2, weight = 1)

        # trainer results
        self.trainerResultInfo = self.buildSimpleLabel(self.resultsBox, tr("page.search.resultsBox.default"))
        self.trainerResultInfo.grid(column = 0, row = 0, columnspan = 3, sticky = (W, N, E, S), padx = 5)
        self.trainerLabel = self.buildSimpleLabel(self.resultsBox, tr("page.generic.trainer"))
        self.trainerLabel.grid(column = 0, row = 1, padx = 5, pady = 5)
        self.tclass = StringVar(self.resultsBox)
        self.tclassCombo = self.addSimpleCombobox(self.tclass, self.handleTClassCombo, self.resultsBox, 1, 1)
        self.tclassCombo.state(["disabled"])
        self.tname = StringVar(self.resultsBox)
        self.tnameCombo = self.addSimpleCombobox(self.tname, self.handleTNameCombo, self.resultsBox, 2, 1, padx = 5)
        self.tnameCombo.state(["disabled"])

        # teammate results
        teammateResultsWrapper = ttk.Frame(self.resultsBox)
        self.teammate1ResultBox = TeammateResultFrame(teammateResultsWrapper, self, 1)
        self.teammate2ResultBox = TeammateResultFrame(teammateResultsWrapper, self, 2)
        self.teammate3ResultBox = TeammateResultFrame(teammateResultsWrapper, self, 3)
        self.teammateResultBoxes = [self.teammate1ResultBox, self.teammate2ResultBox, self.teammate3ResultBox]
        self.teammate1ResultBox.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.teammate2ResultBox.grid(column = 1, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.teammate3ResultBox.grid(column = 2, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        teammateResultsWrapper.grid(column = 0, row = 2, columnspan = 3, sticky = (W, N, E, S))
        teammateResultsWrapper.columnconfigure(0, weight = 1)
        teammateResultsWrapper.columnconfigure(1, weight = 1)
        teammateResultsWrapper.columnconfigure(2, weight = 1)
        teammateResultsWrapper.rowconfigure(0, weight = 1)

        # set up initial state
        self.prepFacility()

        # place this tab
        infoLabel = self.buildSimpleLabel(self, tr("page.teammate_matching.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5)
        facilityBox = ttk.Labelframe(self)
        facilityBox.columnconfigure(0, weight = 1)
        facilityBox.rowconfigure(0, weight = 1)
        self.buildFacility(facilityBox)
        self.gridFacility(0, 0)
        facilityBox.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 5)
        self.matchBox.grid(column = 0, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.resultsBox.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)

    # teammate frames share a sort
    def toggleSorting(self):
        self.alpha = not self.alpha
        for teammateBox in self.teammateBoxes:
            self.setSortToggleText()
            self.fillComboboxPlusEmpty(teammateBox.pokeCombo, self.getSorted(), teammateBox.poke)
        self.matchButton['text'] = tr("page.teammate_matching.matchButton")

    def prepFacility(self):
        self.battlenumAtMatchTime = data.emptyKey

    # when the facility selection changes, tells everything to update
    def handleFacility(self):
        self.currentResultsA = ndict()
        self.fillComboboxKeys(self.tclassCombo, self.currentResultsA, self.tclass)
        self.prepFacility()
        self.trainerResultInfo['text'] = tr("page.search.resultsBox.default")
        for teammateBox in self.teammateBoxes:
            teammateBox.handleFacility()
        for teammateResultBox in self.teammateResultBoxes:
            teammateResultBox.handleFacility()

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self, event = None):
        self.setToolTip(self.tclassCombo, self.tclass.get())
        tnameData = self.currentResultsA[self.tclass.get()]
        self.fillComboboxKeys(self.tnameCombo, tnameData, self.tname)

    # when the trainer name combo box updates, tells the teammate results combo boxes to update
    def handleTNameCombo(self, event = None):
        self.setToolTip(self.tnameCombo, self.tname.get())
        self.teammate1ResultBox.updateResultsCombo(self.currentResultsA[self.tclass.get()][self.tname.get()]['1'], self.teammate1Box.pokeCombo.current() == 0)
        self.teammate2ResultBox.updateResultsCombo(self.currentResultsA[self.tclass.get()][self.tname.get()]['2'], self.teammate2Box.pokeCombo.current() == 0)
        self.teammate3ResultBox.updateResultsCombo(self.currentResultsA[self.tclass.get()][self.tname.get()]['3'], self.teammate3Box.pokeCombo.current() == 0)

    def getResults(self):
        return self.currentResultsA

    def matchChanged(self, event):
        self.matchButton['text'] = tr("page.teammate_matching.matchButton.changed")
        selected_pokes = 0
        for teammateBox in self.teammateBoxes:
            if teammateBox.pokeCombo.current() != 0:
                selected_pokes = selected_pokes + 1
        if selected_pokes >= 2:
            self.matchButton.state(["!disabled"])
        else:
            self.matchButton.state(["disabled"])

    def clearMatch(self):
        for teammateBox in self.teammateBoxes:
            teammateBox.clearMatch()
        self.battlenumCombo.current(0)
        self.matchButton['text'] = tr("page.teammate_matching.matchButton")
        self.matchButton.state(["disabled"])

    def match(self):

        # don't allow searching multiple of the same species
        if len(set([self.teammate1Box.poke.get(), self.teammate2Box.poke.get(), self.teammate3Box.poke.get()])) < 3:
            self.currentResultsA = ndict()
            self.fillComboboxKeys(self.tclassCombo, self.currentResultsA, self.tclass)
            self.matchButton['text'] = tr("page.teammate_matching.matchButton")
            self.trainerResultInfo['text'] = tr("page.teammate_matching.duplicate_species")
            for teammateResultBox in self.teammateResultBoxes:
                teammateResultBox.teammateResultInfo['text'] = tr("page.search.resultsBox.default")
            return

        self.setMainWindowTitleInfo(tr("page.welcome.status.searching"))
        self.update_idletasks()

        self.battlenumAtMatchTime = self.battlenum.get()
        if self.shouldCheck(self.battlenumAtMatchTime):
            search_map = data.battlenumToGroupedSetProviders(self.data.facilities[self.facility])[self.battlenumAtMatchTime]
        else:
            search_map = data.groupedSetProviders(self.data.facilities[self.facility])

        def setMatcher(setProvider, teammateBox, skips):
            matched_sets = []
            sets = data.setsAlphaSortedList(setProvider.sets)

            for pokeset in sets:
                for pswi in skips:
                    if setProvider.iv == pswi.iv and pokeset == pswi.pokeset:
                        continue

                if self.shouldCheck(teammateBox.poke.get()):
                    if pokeset.species.name != teammateBox.poke.get():
                        continue
                if self.shouldCheck(teammateBox.item.get()):
                    if pokeset.item != teammateBox.item.get():
                        continue
                if self.shouldCheck(teammateBox.move1.get()):
                    if teammateBox.move1.get() not in pokeset.moves:
                        continue
                if self.shouldCheck(teammateBox.move2.get()):
                    if teammateBox.move2.get() not in pokeset.moves:
                        continue
                if self.shouldCheck(teammateBox.move3.get()):
                    if teammateBox.move3.get() not in pokeset.moves:
                        continue
                if self.shouldCheck(teammateBox.move4.get()):
                    if teammateBox.move4.get() not in pokeset.moves:
                        continue

                matched_sets.append(core.PokeSetWithIV(pokeset, setProvider.iv))

            # sort by iv, putting 31 first
            matched_sets = sorted(matched_sets, key = lambda pswi: -1 if pswi.iv == 31 else pswi.iv)
            # alphabetical sort - sort by name, then set number
            matched_sets = sorted(matched_sets, key = lambda pswi: attrgetter('pokeset.species.name', 'pokeset.pset')(pswi))
            return matched_sets

        # dict of {tclass} to "{tname1}, {tname2}, ..." to {teammate number} to list of pswis
        matchResults = ndict()
        countedTClass = False
        tclassCount = 0
        tnameCount = 0
        for tclass, nextDict in search_map.items():
            countedTClass = False
            for tnames, setProvider in nextDict.items():
                teammate1Matches = []
                if self.shouldCheck(self.teammate1Box.poke.get()):
                    teammate1Matches = setMatcher(setProvider, self.teammate1Box, [])
                    if len(teammate1Matches) < 1:
                        continue
                teammate2Matches = []
                if self.shouldCheck(self.teammate2Box.poke.get()):
                    teammate2Matches = setMatcher(setProvider, self.teammate2Box, teammate1Matches)
                    if len(teammate2Matches) < 1:
                        continue
                teammate3Matches = []
                if self.shouldCheck(self.teammate3Box.poke.get()):
                    teammate3Matches = setMatcher(setProvider, self.teammate3Box, teammate1Matches + teammate2Matches)
                    if len(teammate3Matches) < 1:
                        continue

                if len(teammate1Matches) < 1 and len(teammate2Matches) < 1 and len(teammate3Matches) < 1:
                    continue

                if not countedTClass:
                    tclassCount = tclassCount + 1
                    countedTClass = True
                tnameCount = tnameCount + len(tnames.split(","))
                # would be nice to get a 'true' unique trainer count (some trainers that are different classes actually have the same sets, particularly in factory)
                # but that would imply that the tclass/tname comboboxes would have to be turned into a single box? and also would require me to calculate that information which seems like it would take a number of seconds.

                matchResults[tclass][tnames]['1'] = teammate1Matches
                matchResults[tclass][tnames]['2'] = teammate2Matches
                matchResults[tclass][tnames]['3'] = teammate3Matches

        self.currentResultsA = matchResults
        self.fillComboboxKeys(self.tclassCombo, self.currentResultsA, self.tclass)

        self.matchButton['text'] = tr("page.teammate_matching.matchButton")
        if tnameCount > 0:
            self.trainerResultInfo['text'] = tr("page.teammate_matching.resultsBox.done", tnameCount, tclassCount)
        else:
            self.trainerResultInfo['text'] = tr("page.teammate_matching.empty_results")

        self.setMainWindowTitleInfo(None)
        self.update_idletasks()

    def shouldCheck(self, value):
        return value != '' and value != data.emptyKey

    def jump(self, number):
        if number < 0 or number > 3:
            return
        if len(self.teammateResultBoxes[number - 1].teammateResult.get()) < 1:
            return

        self._root().browseTrainerSetsPage.facilityVar.set(self.facilityVar.get())
        self._root().browseTrainerSetsPage.setFacility()
        self._root().browseTrainerSetsPage.battlenumCombo.set(self.battlenumAtMatchTime)
        self._root().browseTrainerSetsPage.battlenumCombo.event_generate("<<ComboboxSelected>>")
        self._root().browseTrainerSetsPage.tclassCombo.set(self.tclass.get())
        self._root().browseTrainerSetsPage.tclassCombo.event_generate("<<ComboboxSelected>>")
        self._root().browseTrainerSetsPage.tnameCombo.set(self.tname.get())
        self._root().browseTrainerSetsPage.tnameCombo.event_generate("<<ComboboxSelected>>")

        pswi = self.currentResultsA[self.tclass.get()][self.tname.get()][str(number)][self.teammateResultBoxes[number - 1].teammateResultCombo.current()]

        self._root().browseTrainerSetsPage.pokeCombo.set(pswi.pokeset.species.name)
        self._root().browseTrainerSetsPage.pokeCombo.event_generate("<<ComboboxSelected>>")
        self._root().browseTrainerSetsPage.set.set(pswi.pokeset.pset)
        self._root().browseTrainerSetsPage.handleSetRadio()

        self._root().nonhallTabs.select(1)

# frame for each teammate matching options
class TeammateFrame(ttk.Labelframe):
    def __init__(self, parent, parentpage, number):
        self.parentpage = parentpage
        self.number = number
        super().__init__(parent, text = tr("page.teammate_matching.teammate_num", self.number), padding = 5)

        self.columnconfigure(0, weight = 1)
        for i in range(0, 10):
            self.rowconfigure(i, weight = 1)

        # pokemon
        self.parentpage.addSimpleLabel(self, tr("page.generic.pokemon"), 0, 0)
        self.poke = StringVar(self)
        self.pokeCombo = self.addMatchCombobox(self.poke, self, self.parentpage.getSorted(), 0, 2)
        # held item
        self.parentpage.addSimpleLabel(self, tr("page.search.item"), 0, 3)
        self.item = StringVar(self)
        self.itemCombo = self.addMatchCombobox(self.item, self, self.parentpage.items, 0, 4)
        self.itemCombo.state(["disabled"])
        # moves
        self.parentpage.addSimpleLabel(self, tr("page.search.moves"), 0, 5)
        self.move1 = StringVar(self)
        self.moveCombo1 = self.addMatchCombobox(self.move1, self, self.parentpage.moves, 0, 6)
        self.move2 = StringVar(self)
        self.moveCombo2 = self.addMatchCombobox(self.move2, self, self.parentpage.moves, 0, 7)
        self.move3 = StringVar(self)
        self.moveCombo3 = self.addMatchCombobox(self.move3, self, self.parentpage.moves, 0, 8)
        self.move4 = StringVar(self)
        self.moveCombo4 = self.addMatchCombobox(self.move4, self, self.parentpage.moves, 0, 9)
        self.moveCombos = [self.moveCombo1, self.moveCombo2, self.moveCombo3, self.moveCombo4]
        for moveCombo in self.moveCombos:
            moveCombo.state(["disabled"])

    # adds a match combobox connected to matchChanged
    def addMatchCombobox(self, var, parent, contents, column, row):
        # must fill before binding command, otherwise it causes problems
        combo = self.parentpage.addSimpleCombobox(var, None, parent, column, row, padx = 5)
        self.parentpage.fillComboboxPlusEmpty(combo, contents, var)
        combo.bind('<<ComboboxSelected>>', self.matchChanged)
        return combo

    def matchChanged(self, event):
        if self.poke.get() == data.emptyKey:
            self.itemCombo.current(0)
            self.itemCombo.state(["disabled"])
            for moveCombo in self.moveCombos:
                moveCombo.current(0)
                moveCombo.state(["disabled"])
        else:
            if self.parentpage.facility != core.Facility.Arcade:
                self.itemCombo.state(["!disabled"])
            for moveCombo in self.moveCombos:
                moveCombo.state(["!disabled"])
        self.parentpage.matchChanged(None)

    def clearMatch(self):
        self.pokeCombo.current(0)
        # manually generate the combobox selected event
        self.pokeCombo.event_generate("<<ComboboxSelected>>")

    def handleFacility(self):
        if self.parentpage.facility == core.Facility.Arcade:
            self.itemCombo.current(0)
            self.itemCombo.state(["disabled"])
        elif self.pokeCombo.current() != 0:
            self.itemCombo.state(["!disabled"])

# frame for each teammate matching results
class TeammateResultFrame(ttk.Labelframe):
    def __init__(self, parent, parentpage, number):
        self.parentpage = parentpage
        self.number = number
        super().__init__(parent, text = tr("page.teammate_matching.teammate_num_match", self.number), padding = 5)

        self.columnconfigure(0, weight = 1)
        for i in range(0, 3):
            self.rowconfigure(i, weight = 1)

        # teammate output
        self.teammateResultInfo = self.parentpage.buildSimpleLabel(self, tr("page.search.resultsBox.default"))
        self.teammateResultInfo.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5)
        self.teammateResult = StringVar(self)
        self.teammateResultCombo = self.parentpage.addSimpleCombobox(self.teammateResult, self.handleResultsCombo, self, 0, 1, padx = 5, pady = 5)
        self.teammateResultCombo.state(["disabled"])
        self.jumpButton = ttk.Button(self, text = tr("page.teammate_matching.jumpButton"), command = self.jump)
        self.jumpButton.grid(column = 0, row = 2, sticky = (W, E), padx = 5)
        self.jumpButton.state(["disabled"])

    def jump(self):
        self.parentpage.jump(self.number)

    def handleFacility(self):
        self.teammateResultInfo['text'] = tr("page.search.resultsBox.default")
        self.parentpage.fillCombobox(self.teammateResultCombo, tuple(), self.teammateResult)
        self.jumpButton.state(["disabled"])

    def handleResultsCombo(self, event):
        self.parentpage.setToolTip(self.teammateResultCombo, self.teammateResult.get())

    def updateResultsCombo(self, data, notSearched):
        if len(data) == 1:
            self.teammateResultInfo['text'] = tr("page.teammate_matching.resultsBox.setInfo.singular", len(data))
        elif len(data) == 0 and notSearched:
            self.teammateResultInfo['text'] = tr("page.search.resultsBox.default")
        else:
            self.teammateResultInfo['text'] = tr("page.teammate_matching.resultsBox.setInfo.plural", len(data))
        self.parentpage.fillCombobox(self.teammateResultCombo, [pswi.getShowdownNickname() for pswi in data], self.teammateResult)
        if len(data) > 0:
            self.jumpButton.state(["!disabled"])
            self.parentpage.setToolTip(self.jumpButton, tr("page.teammate_matching.jumpButton.tooltip"))
        else:
            self.jumpButton.state(["disabled"])
            self.parentpage.setToolTip(self.jumpButton, "")
