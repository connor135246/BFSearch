# search


from enum import Enum

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QWidget, QLabel, QComboBox, QPushButton, QListView, QSizePolicy
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from bfsearch import core, data
from bfsearch.qt import browse
from bfsearch.translate import tr


# todo: fix the searchBox changing size when you click the pokeCombo sortToggle
class SearchPage(browse.SharedPageElements):
    def __init__(self, parent, the_data):
        super().__init__(parent)

        self.data = the_data

        self.the_list = data.everyIndividualPokemon(self.data.trainers)

        self.setLayout(QVBoxLayout(self))

        self.layout().addWidget(QLabel(tr("page.search.info")))
        usefulLayout = QHBoxLayout()
        self.layout().addLayout(usefulLayout)

        ## search box
        self.searchBox = QGroupBox(tr("page.search.searchBox"))
        self.searchBox.setLayout(QVBoxLayout(self.searchBox))
        usefulLayout.addWidget(self.searchBox)

        # battle number
        self.addLabel(self.searchBox.layout(), tr("page.generic.battle_number"), "")
        self.battlenumCombo = self.addComboBox(self.searchBox.layout(), [battlenum.value for battlenum in list(core.BattleNum)])

        # trainer class and name
        # this is the only one that updates as you select it. tclass links to possible tnames.
        self.addLabel(self.searchBox.layout(), tr("page.generic.trainer"), "")
        self.trainerDict = {data.emptyKey : data.allTrainerNames(self.data.trainers)}
        self.trainerDict.update(data.tclassToTName(self.data.trainers))
        self.tclassCombo = QComboBox()
        self.searchBox.layout().addWidget(self.tclassCombo)
        self.tclassCombo.currentTextChanged.connect(self.handleTClassCombo)
        self.tnameCombo = QComboBox()
        self.searchBox.layout().addWidget(self.tnameCombo)
        self.tnameCombo.currentTextChanged.connect(self.searchChanged)

        # pokemon
        self.addLabel(self.searchBox.layout(), tr("page.generic.pokemon"), "")
        self.sortedAlpha = data.allPokemonAlpha(self.data.sets)
        self.sortedDex = data.allPokemonDex(self.data.sets)
        self.searchBox.layout().addWidget(self.sortToggle)
        self.pokeCombo = self.addComboBox(self.searchBox.layout(), self.getSorted())

        # held item
        self.addLabel(self.searchBox.layout(), tr("page.search.item"), "")
        self.itemCombo = self.addComboBox(self.searchBox.layout(), data.allItems(self.data.sets))

        # moves
        self.addLabel(self.searchBox.layout(), tr("page.search.moves"), "")
        self.moveCombo1 = self.addComboBox(self.searchBox.layout(), data.allMoves(self.data.sets))
        self.moveCombo2 = self.addComboBox(self.searchBox.layout(), data.allMoves(self.data.sets))
        self.moveCombo3 = self.addComboBox(self.searchBox.layout(), data.allMoves(self.data.sets))
        self.moveCombo4 = self.addComboBox(self.searchBox.layout(), data.allMoves(self.data.sets))

        # search!
        self.searchBox.layout().addSpacing(10)
        self.searchButton = QPushButton(tr("page.search.searchButton"))
        self.searchButton.clicked.connect(self.search)
        self.searchBox.layout().addWidget(self.searchButton)
        self.clearSearchButton = QPushButton(tr("page.search.clearSearchButton"))
        self.clearSearchButton.clicked.connect(self.clearSearch)
        self.searchBox.layout().addWidget(self.clearSearchButton)

        ## results box
        self.resultsBox = QGroupBox(tr("page.search.resultsBox"))
        self.resultsBox.setLayout(QVBoxLayout(self.resultsBox))
        usefulLayout.addWidget(self.resultsBox)

        # results info
        self.resultsInfo = QLabel(tr("page.search.resultsBox.default"))
        self.resultsBox.layout().addWidget(self.resultsInfo)

        # results sorting
        # alphabetically organized results
        self.currentResultsA = []
        # dex number organized results
        self.currentResultsD = []
        # sort toggle button
        self.resultSortToggle = QPushButton("")
        self.resultsAlpha = True
        self.setResultsToggleText()
        self.resultSortToggle.clicked.connect(self.toggleResultSorting)
        self.resultSortToggle.setToolTip(tr("page.search.sortToggle.tooltip"))
        self.resultsBox.layout().addWidget(self.resultSortToggle)

        # results combo
        self.resultsCombo = QComboBox()
        self.resultsBox.layout().addWidget(self.resultsCombo)
        self.resultsCombo.currentTextChanged.connect(self.handleResultsCombo)
        self.resultsCombo.setEnabled(False)

        # output
        self.output.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.resultsBox.layout().addWidget(self.output, stretch = 1)

        # clipboard options
        self.currentIV = 31
        self.resultsBox.layout().addLayout(self.clipboardOptions)

        # trainer output
        self.trainerInfo = QLabel()
        self.resultsBox.layout().addWidget(self.trainerInfo)
        self.trainerOutput = QStandardItemModel(0, 1, self.resultsBox)
        trainerOutputView = QListView()
        trainerOutputView.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        trainerOutputView.setModel(self.trainerOutput)
        self.resultsBox.layout().addWidget(trainerOutputView)

        # set up initial state
        self.tclassCombo.addItems(self.trainerDict.keys())
        self.updateSet()
        self.searchButton.setText(tr("page.search.searchButton"))
        self.trainerInfo.setText(tr("page.search.resultsBox.default"))

    def addComboBox(self, layout, contents):
        combo = QComboBox()
        layout.addWidget(combo)
        self.fillComboList(combo, contents)
        combo.currentTextChanged.connect(self.searchChanged)
        return combo

    def addLabel(self, layout, name, tooltip):
        label = QLabel(name)
        label.setToolTip(tooltip)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return label

    # sets the combo box to the list, plus an empty entry at the start
    def fillComboList(self, combo, contents):
        combo.clear()
        combo.addItem(data.emptyKey)
        combo.addItems(contents)
        combo.setEnabled(combo.count() > 1)

    def toggleSorting(self):
        super().toggleSorting()
        self.fillComboList(self.pokeCombo, self.getSorted())

    def toggleResultSorting(self):
        self.resultsAlpha = not self.resultsAlpha
        self.setResultsToggleText()
        self.fillResultsCombo()

    def setResultsToggleText(self):
        if self.resultsAlpha:
            self.resultSortToggle.setText(tr("page.search.sortToggle.alpha"))
        else:
            self.resultSortToggle.setText(tr("page.search.sortToggle.dex"))

    def getResults(self):
        return self.getResultsAlpha() if self.resultsAlpha else self.getResultsDex()

    def getResultsAlpha(self):
        return self.currentResultsA

    def getResultsDex(self):
        return self.currentResultsD

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self):
        self.searchChanged()
        tnameData = data.digForData(self.trainerDict, [self.tclassCombo.currentText()])
        if tnameData is not None:
            self.fillComboList(self.tnameCombo, tnameData)
        else:
            self.fillComboList(self.tnameCombo, data.allTrainerNames(self.data.trainers))

    def fillResultsCombo(self):
        self.resultsCombo.clear()
        for pswi, _ in self.getResults():
            self.resultsCombo.addItem(pswi.getShowdownNickname())
        self.resultsCombo.setEnabled(self.resultsCombo.count() > 1)

    def handleResultsCombo(self):
        self.updateSet()

    def getIV(self):
        return self.currentIV

    def updateSet(self):
        super().updateSet()
        if self.resultsCombo.count() > 0 and self.resultsCombo.currentIndex() < len(self.getResults()):
            pswi, trainers = self.getResults()[self.resultsCombo.currentIndex()]
            self.currentSet = pswi.pokeset
            self.currentIV = pswi.iv
            self.output.setText(browse.getSetResultString(self.currentSet, self.currentIV, self.itemCheck.isChecked()))
            self.trainerOutput.clear()
            for trainer in trainers:
                self.trainerOutput.appendRow(QStandardItem(str(trainer)))
            if len(trainers) == 1:
                self.trainerInfo.setText(tr("page.search.resultsBox.trainerInfo.singular", len(trainers)))
            else:
                self.trainerInfo.setText(tr("page.search.resultsBox.trainerInfo.plural", len(trainers)))
            self.clipboardButton.setEnabled(True)
            self.resultsCombo.setToolTip(self.resultsCombo.currentText())
        else:
            self.clearResults()

    def clearResults(self):
        self.clipboardButton.setEnabled(False)
        self.resultsCombo.setToolTip("")
        self.trainerOutput.clear()
        self.trainerInfo.setText(tr("page.search.resultsBox.trainerInfo.plural", 0))

    def searchChanged(self):
        self.searchButton.setText(tr("page.search.searchButton.changed"))

    def clearSearch(self):
        self.battlenumCombo.setCurrentIndex(0)
        self.tclassCombo.setCurrentIndex(0)
        self.tnameCombo.setCurrentIndex(0)
        self.pokeCombo.setCurrentIndex(0)
        self.itemCombo.setCurrentIndex(0)
        self.moveCombo1.setCurrentIndex(0)
        self.moveCombo2.setCurrentIndex(0)
        self.moveCombo3.setCurrentIndex(0)
        self.moveCombo4.setCurrentIndex(0)
        self.searchButton.setText(tr("page.search.searchButton"))

    def search(self):
        # grouping of combobox, reducer, and nice name
        class SearchOption(Enum):
            BattleNum = (self.battlenumCombo, self.reduceBattleNum, "Battle Number")
            TClass = (self.tclassCombo, self.reduceTClass, "Trainer Class")
            TName = (self.tnameCombo, self.reduceTName, "Trainer Name")
            Species = (self.pokeCombo, self.reducePoke, "Pokemon")
            Item = (self.itemCombo, self.reduceItem, "Item")
            Move1 = (self.moveCombo1, self.reduceMove1, "Move")
            Move2 = (self.moveCombo2, self.reduceMove2, "Move")
            Move3 = (self.moveCombo3, self.reduceMove3, "Move")
            Move4 = (self.moveCombo4, self.reduceMove4, "Move")

        searchByStage = [(None, len(self.the_list) > 0, self.the_list)]
        if not searchByStage[-1][1]:
            self.emptyResults(searchByStage)
        else:
            for searchoption in list(SearchOption):
                searchByStage = self.checkAndReduce(searchoption, searchByStage)
                if len(searchByStage[-1][2]) < 1:
                    self.emptyResults(searchByStage)
                    break

        searchResults = searchByStage[-1][2]
        currentResults = data.groupUniquePokemon(searchResults)
        self.currentResultsA = sorted(currentResults, key = lambda unique : unique[0].getShowdownNickname())
        self.currentResultsD = sorted(currentResults, key = lambda unique : unique[0].dexSortValue())
        self.fillResultsCombo()

        self.resultsInfo.setText(tr("page.search.resultsBox.done", len(searchResults), len(currentResults)))
        self.searchButton.setText(tr("page.search.searchButton"))

    def checkAndReduce(self, searchoption, searchByStage):
        previousResult = searchByStage[-1][2]
        this_check = len(previousResult) > 0 and self.shouldCheck(searchoption.value[0].currentText())
        if this_check:
            this_result = searchoption.value[1].__call__(previousResult)
        else:
            this_result = previousResult
        return searchByStage + [(searchoption, this_check, this_result)]

    def shouldCheck(self, value):
        return value != '' and value != data.emptyKey

    def emptyResults(self, searchByStage):
        string = tr("page.search.result.none") + "\n\n"
        prefixCharacter = ">"
        count = 1
        for searchoption, check, result in searchByStage:
            if searchoption is None:
                string += tr("page.search.result.initial", len(result)) + "\n"
                if not check:
                    string += "  "*count + "-> " + tr("page.search.result.initial.none") + "\n"
                    count += 1
            elif check:
                string += "  "*count + "-> " + tr("page.search.result.option", len(result), searchoption.value[2], searchoption.value[0].currentText()) + "\n"
                count += 1
        self.output.setText(string)

    def reduceBattleNum(self, search_list):
        try:
            battlenum = core.BattleNum(self.battlenumCombo.currentText())
            return [tps for tps in search_list if battlenum in tps.trainer.battlenums]
        except ValueError:
            return search_list

    def reduceTClass(self, search_list):
        return [tps for tps in search_list if self.tclassCombo.currentText() == tps.trainer.tclass]

    def reduceTName(self, search_list):
        return [tps for tps in search_list if self.tnameCombo.currentText() == tps.trainer.tname]

    def reducePoke(self, search_list):
        return [tps for tps in search_list if self.pokeCombo.currentText() == tps.pokeset.species.name]

    def reduceItem(self, search_list):
        return [tps for tps in search_list if self.itemCombo.currentText() == tps.pokeset.item]

    def reduceMove1(self, search_list):
        return [tps for tps in search_list if self.moveCombo1.currentText() in tps.pokeset.moves]
    def reduceMove2(self, search_list):
        return [tps for tps in search_list if self.moveCombo2.currentText() in tps.pokeset.moves]
    def reduceMove3(self, search_list):
        return [tps for tps in search_list if self.moveCombo3.currentText() in tps.pokeset.moves]
    def reduceMove4(self, search_list):
        return [tps for tps in search_list if self.moveCombo4.currentText() in tps.pokeset.moves]
