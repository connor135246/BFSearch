# browsehall


import math

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSpinBox, QGroupBox
from PySide6.QtCore import Qt

from bfsearch import core, data
from bfsearch.qt import browse
from bfsearch.translate import tr


# base page for single hall set browsing
# very similar to browse.BrowseSetsPageBase
class BrowseHallSetsPageBase(browse.SharedPageElements):
    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QVBoxLayout(self))

        mainBox = QGroupBox("")
        self.mainLayout = QVBoxLayout(mainBox)
        mainBox.setLayout(self.mainLayout)
        self.layout().addWidget(mainBox)

        # sort toggle
        self.mainLayout.addWidget(self.sortToggle)

        ## pokemon selector
        setSelect = QHBoxLayout()
        self.mainLayout.addLayout(setSelect)

        # species combo box
        self.pokeLabel = QLabel(tr("page.generic.pokemon"))
        self.pokeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setSelect.addWidget(self.pokeLabel)
        self.pokeCombo = self.addComboBox(self.handlePokeCombo, setSelect)

        # level spin box
        self.levelLabel = QLabel(tr("page.hall_sets.level"))
        self.levelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setSelect.addWidget(self.levelLabel)
        self.levelBox = QSpinBox()
        self.levelBox.setRange(30, 96)
        self.levelBox.setValue(96)
        self.levelBox.valueChanged.connect(self.handleLevelBox)
        setSelect.addWidget(self.levelBox)

        # iv spin box
        self.ivLabel = QLabel(tr("page.all_sets.ivs"))
        self.ivLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setSelect.addWidget(self.ivLabel)
        self.ivBox = QSpinBox()
        self.ivBox.setRange(0, 31)
        self.ivBox.setValue(31)
        self.ivBox.valueChanged.connect(self.handleIVBox)
        setSelect.addWidget(self.ivBox)

        # output
        self.mainLayout.addWidget(self.output)

        # clipboard options
        self.mainLayout.addLayout(self.clipboardOptions)
        self.itemCheck.hide()

    def addComboBox(self, connect, layout):
        combo = QComboBox()
        combo.currentTextChanged.connect(connect)
        layout.addWidget(combo)
        return combo

    # sets the combo box to the keys of contents
    def fillComboKeys(self, combo, contents):
        combo.clear()
        for key in contents.keys():
            combo.addItem(str(key))
        combo.setEnabled(combo.count() > 1)

    def toggleSorting(self):
        super().toggleSorting()
        self.fillComboKeys(self.pokeCombo, self.getSorted())

    def setupIVBox(self, minIV, maxIV):
        self.ivBox.setRange(minIV, maxIV)
        if self.ivBox.minimum() == self.ivBox.maximum():
            self.ivBox.setToolTip(tr("page.all_sets.ivBox.tooltip.fixed"))
            self.ivBox.setEnabled(False)
        else:
            self.ivBox.setToolTip(tr("page.generic.range", self.ivBox.minimum(), self.ivBox.maximum()))
            self.ivBox.setEnabled(True)

    def getIV(self):
        return self.ivBox.value()

    def handlePokeCombo(self):
        self.updateSet()

    def handleIVBox(self):
        self.updateSet()

    def handleLevelBox(self):
        self.updateSet()

    def updateSet(self):
        super().updateSet()
        self.currentSet = data.digForData(self.getSorted(), [self.pokeCombo.currentText()])
        if self.currentSet is not None:
            self.output.setText(browse.getSetResultString(self.currentSet, self.ivBox.value(), self.itemCheck.isChecked(), self.levelBox.value()))
            self.clipboardButton.setEnabled(True)
            self.pokeCombo.setToolTip(str(self.currentSet.species))
        else:
            self.clearResults()

    def clearResults(self):
        self.output.setText(tr("page.all_sets.empty_results"))
        self.clipboardButton.setEnabled(False)
        self.pokeCombo.setToolTip("")


# browse all hall sets
class BrowseAllHallSetsPage(BrowseHallSetsPageBase):
    def __init__(self, parent, hallSetProvider):
        super().__init__(parent)

        # set up
        self.hallSetProvider = hallSetProvider
        self.sortedAlpha = data.hallSetsAlphaSorted(self.hallSetProvider.sets)
        self.sortedDex = data.hallSetsDexSorted(self.hallSetProvider.sets)
        self.setupIVBox(0, 31)

        self.layout().insertWidget(0, QLabel(tr("page.hall_sets.info")))
        self.pokeLabel.setToolTip(tr("page.hall_sets.pokemon.tooltip"))
        self.levelLabel.setToolTip(tr("page.hall_sets.level.tooltip"))
        self.levelBox.setToolTip(tr("page.generic.range", self.levelBox.minimum(), self.levelBox.maximum()))
        self.ivLabel.setToolTip(tr("page.hall_sets.ivs.tooltip"))

        # initial state
        self.fillComboKeys(self.pokeCombo, self.getSorted())
        self.pokeCombo.setCurrentText("Weavile")


# browse hall sets by type and rank, plus argenta
class CalcHallSetsPage(BrowseHallSetsPageBase):

    HALL_BRAIN_SILVER = "Hall Matron Argenta (Silver Print)"
    HALL_BRAIN_GOLD = "Hall Matron Argenta (Gold Print)"

    def __init__(self, parent, typeToRankToHallSets, hallSetGroupToHallSets):
        super().__init__(parent)

        self.typeToRankToHallSets = typeToRankToHallSets
        self.hallSetGroupToHallSets = hallSetGroupToHallSets

        ## your pokemon's info
        pokeInfo = QHBoxLayout()
        self.mainLayout.insertLayout(0, pokeInfo)

        # your level spin box
        self.yourLevelLabel = QLabel(tr("page.hall_calc.your_level"))
        self.yourLevelLabel.setToolTip(tr("page.hall_calc.your_level.tooltip"))
        self.yourLevelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pokeInfo.addWidget(self.yourLevelLabel)
        self.yourLevelBox = QSpinBox()
        self.yourLevelBox.setRange(30, 100)
        self.yourLevelBox.setValue(50)
        self.yourLevelBox.valueChanged.connect(self.handleYourLevelBox)
        pokeInfo.addWidget(self.yourLevelBox)

        # your bst combo box
        self.yourBSTLabel = QLabel(tr("page.hall_calc.your_bst"))
        self.yourBSTLabel.setToolTip(tr("page.hall_calc.your_bst.tooltip"))
        self.yourBSTLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pokeInfo.addWidget(self.yourBSTLabel)
        self.yourBSTCombo = self.addComboBox(self.handleYourBSTCombo, pokeInfo)

        ## battle selector
        battleSelect = QHBoxLayout()
        self.mainLayout.insertLayout(1, battleSelect)

        # type combo box
        self.typeLabel = QLabel(tr("page.hall_calc.type"))
        self.typeLabel.setToolTip(tr("page.hall_calc.type.tooltip"))
        self.typeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        battleSelect.addWidget(self.typeLabel)
        self.typeCombo = self.addComboBox(self.handleTypeCombo, battleSelect)

        # rank spin box
        self.rankLabel = QLabel(tr("page.hall_calc.rank"))
        self.rankLabel.setToolTip(tr("page.hall_calc.rank.tooltip"))
        self.rankLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        battleSelect.addWidget(self.rankLabel)
        self.rankBox = QSpinBox()
        self.rankBox.setRange(1, 10)
        self.rankBox.setValue(1)
        self.rankBox.valueChanged.connect(self.handleRankBox)
        battleSelect.addWidget(self.rankBox)

        # visited types spin box
        self.visitedTypesLabel = QLabel(tr("page.hall_calc.visited_types"))
        self.visitedTypesLabel.setToolTip(tr("page.hall_calc.visited_types.tooltip"))
        self.visitedTypesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        battleSelect.addWidget(self.visitedTypesLabel)
        self.visitedTypesBox = QSpinBox()
        self.visitedTypesBox.setRange(0, 17)
        self.visitedTypesBox.setValue(0)
        self.visitedTypesBox.valueChanged.connect(self.handleVisitedTypesBox)
        battleSelect.addWidget(self.visitedTypesBox)

        # set up
        self.layout().insertWidget(0, QLabel(tr("page.hall_calc.info")))
        self.pokeLabel.setToolTip(tr("page.hall_calc.pokemon.tooltip"))
        self.levelLabel.setToolTip(tr("page.hall_calc.level.tooltip"))
        self.yourLevelBox.setToolTip(tr("page.generic.range", self.yourLevelBox.minimum(), self.yourLevelBox.maximum()))
        self.rankBox.setToolTip(tr("page.generic.range", self.rankBox.minimum(), self.rankBox.maximum()))
        self.visitedTypesBox.setToolTip(tr("page.generic.range", self.visitedTypesBox.minimum(), self.visitedTypesBox.maximum()))
        self.levelBox.setToolTip(tr("page.hall_calc.levelBox.tooltip.fixed"))
        self.ivLabel.setToolTip(tr("page.hall_calc.ivs.tooltip"))

        # initial state
        self.levelBox.setEnabled(False)
        for hallsetgroup in list(core.HallSetGroup):
            self.yourBSTCombo.addItem(hallsetgroup.fullname())
        self.fillComboKeys(self.typeCombo, self.tTRTHS())
        self.typeCombo.addItem(self.HALL_BRAIN_SILVER)
        self.typeCombo.addItem(self.HALL_BRAIN_GOLD)

    # for checking by type/rank
    def tTRTHS(self):
        return self.typeToRankToHallSets

    # for checking frontier brain
    def hSGTHS(self):
        return self.hallSetGroupToHallSets

    def checkingBrain(self):
        return self.typeCombo.currentText() == self.HALL_BRAIN_SILVER or self.typeCombo.currentText() == self.HALL_BRAIN_GOLD

    # when your bst combo box updates, if type is a hall brain, updates the poke combo box
    def handleYourBSTCombo(self):
        if self.checkingBrain():
            self.updateCalcSets()

    # when your level box updates, updates opp level
    def handleYourLevelBox(self):
        self.updateCalcLevel()

    # when type combo box updates, tells the poke combo box to update
    def handleTypeCombo(self):
        # brain doesn't have rank
        self.rankBox.setEnabled(not self.checkingBrain())
        self.updateCalcSets()

    # when rank box updates, tells the poke combo box to update
    def handleRankBox(self):
        self.updateCalcSets()

    # when visited types box updates, updates opp level
    def handleVisitedTypesBox(self):
        self.updateCalcLevel()

    def updateCalcLevel(self):
        if self.checkingBrain():
            self.levelBox.setValue(self.yourLevelBox.value())
        else:
            self.levelBox.setValue(calcOppLevel(self.yourLevelBox.value(), self.rankBox.value(), self.visitedTypesBox.value()))

    def updateCalcIV(self):
        if self.checkingBrain():
            iv = 31
        else:
            iv = ivFromRank(self.rankBox.value())
        self.setupIVBox(iv, iv)

    def updateCalcSets(self):
        if self.checkingBrain():
            if self.typeCombo.currentText() == self.HALL_BRAIN_GOLD:
                currentHallSets = data.digForData(self.hSGTHS(), [core.HallSetGroup.plus500.fullname()])
            else:
                currentHallSets = data.digForData(self.hSGTHS(), [self.yourBSTCombo.currentText()])
        else:
            currentHallSets = data.digForData(self.tTRTHS(), [self.typeCombo.currentText(), self.rankBox.value()])
        if currentHallSets is not None:
            self.sortedAlpha = data.hallSetsAlphaSorted(currentHallSets)
            self.sortedDex = data.hallSetsDexSorted(currentHallSets)
            # when the type/rank/brain selection updates, tells the poke combo box to update
            self.fillComboKeys(self.pokeCombo, self.getSorted())
            self.updateCalcLevel()
            self.updateCalcIV()
            self.typeCombo.setToolTip(self.typeCombo.currentText())
            self.yourBSTCombo.setToolTip(self.yourBSTCombo.currentText())
        else:
            self.clearCalcSetsResults()

    def clearCalcSetsResults(self):
        self.fillComboKeys(self.pokeCombo, {})
        self.typeCombo.setToolTip("")
        self.yourBSTCombo.setToolTip("")

def ivFromRank(rank):
    # start at 8 and go up 2 per rank up to 26
    return 6 + rank * 2

# visitedTypes is the number of types that been been visited before and are therefore above rank 1.
def calcOppLevel(playerLevel, rank, visitedTypes):
    # we want to know the number of types that are above rank 1 - other than this one.
    numberOfTypesAboveRank1ExcludingThisOne = None
    # if we're checking ranks above 1, then the "number of types above rank 1" count includes the current rank, which it shouldn't, so we subtract 1.
    if rank > 1:
        numberOfTypesAboveRank1ExcludingThisOne = visitedTypes - 1
    # if we're checking rank 1, then the "number of types above rank 1" count already does not include the current rank.
    else:
        numberOfTypesAboveRank1ExcludingThisOne = visitedTypes

    baseLevel = playerLevel - 3 * math.sqrt(playerLevel)
    incrementPerRank = math.sqrt(playerLevel) / 5
    maxLevel = math.ceil( baseLevel + max(numberOfTypesAboveRank1ExcludingThisOne, 0) / 2 + ( rank - 1 ) * incrementPerRank )
    return min(playerLevel, maxLevel)
