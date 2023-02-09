# browsehall


import math

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSpinBox, QGroupBox
from PySide6.QtCore import Qt

from bfsearch import data
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


def ivFromRank(rank):
    if rank < 1 or rank > 10:
        raise ValueError(f"Invalid type rank: {rank}")
    return 6 + rank * 2

def calcOppLevel(playerLevel, rank, otherTypesVisited):
	maxLevel = math.ceil( playerLevel - 3 * math.sqrt(playerLevel) + otherTypesVisited / 2 + ( rank - 1 ) * math.sqrt(playerLevel) / 5 )
	return min(playerLevel, maxLevel)
