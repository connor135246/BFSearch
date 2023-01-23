# browse


import math

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QTabWidget, QMainWindow, QDockWidget, QToolBar, QMessageBox, QLabel, QComboBox, QTextEdit, QSizePolicy, QPushButton, QSpinBox, QCheckBox
from PySide6.QtGui import QIcon, QAction, QActionGroup, QGuiApplication
from PySide6.QtCore import Qt, QSize

from bfsearch import data
from bfsearch.translate import tr


# base page for single set browsing
class BrowseSetsPageBase(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # alphabetically organized sets
        self.setsA = {}
        # dex number organized sets
        self.setsD = {}
        
        self.setLayout(QVBoxLayout(self))

        # sort toggle button
        self.sortToggle = QPushButton("")
        self.alpha = True
        self.setSortToggleText()
        self.sortToggle.clicked.connect(self.toggleSorting)
        self.layout().addWidget(self.sortToggle)
        self.sortToggle.setToolTip(tr("page.all_sets.sortToggle.tooltip"))

        setSelect = QHBoxLayout()
        self.layout().addLayout(setSelect)

        # species & set combo boxes
        self.pokeLabel = QLabel(tr("page.all_sets.pokemon"))
        self.pokeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setSelect.addWidget(self.pokeLabel)
        self.pokeCombo = self.addComboBox(self.handlePokeCombo, setSelect)
        self.setCombo = self.addComboBox(self.handleSetCombo, setSelect)

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
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout().addWidget(self.output)

        bottomOptions = QHBoxLayout()
        self.layout().addLayout(bottomOptions)

        # copy to clipboard button
        self.clipboardButton = QPushButton("")
        self.clipboardButton.clicked.connect(self.copyToClipboard)
        bottomOptions.addWidget(self.clipboardButton, stretch = 1)
        # current set (for copy to clipboard)
        self.currentSet = None

        # hide held items checkbox
        self.itemCheck = QCheckBox(tr("page.all_sets.itemCheck"))
        self.itemCheck.stateChanged.connect(self.handleItemCheck)
        bottomOptions.addWidget(self.itemCheck)
        self.itemCheck.setToolTip(tr("page.all_sets.itemCheck.tooltip"))

        # set up initial state
        self.updateSet()

    def addComboBox(self, connect, layout):
        combo = QComboBox()
        combo.currentTextChanged.connect(connect)
        layout.addWidget(combo)
        return combo

    # sets the combo box data to the keys of the data
    def fillComboKeys(self, combo, data):
        combo.clear()
        for key in data.keys():
            combo.addItem(str(key))
        combo.setEnabled(combo.count() > 1)

    def setupIVBox(self, setProvider):
        self.ivBox.setRange(setProvider.minIV, setProvider.maxIV)
        if self.ivBox.minimum() == self.ivBox.maximum():
            self.ivBox.setToolTip(tr("page.all_sets.ivBox.tooltip.fixed"))
            self.ivBox.setEnabled(False)
        else:
            self.ivBox.setToolTip(tr("page.all_sets.ivBox.tooltip.range", [self.ivBox.minimum(), self.ivBox.maximum()]))
            self.ivBox.setEnabled(True)

    def toggleSorting(self):
        self.alpha = not self.alpha
        self.fillComboKeys(self.pokeCombo, self.getSets())
        self.setSortToggleText()

    def setSortToggleText(self):
        if self.alpha:
            self.sortToggle.setText(tr("page.all_sets.sortToggle.alpha"))
        else:
            self.sortToggle.setText(tr("page.all_sets.sortToggle.dex"))

    def getSets(self):
        return self.getSetsAlpha() if self.alpha else self.getSetsDex()

    def getSetsAlpha(self):
        return self.setsA

    def getSetsDex(self):
        return self.setsD

    # when the species combo box updates, tells the set combo box to update
    def handlePokeCombo(self):
        setsData = data.digForData(self.getSets(), [self.pokeCombo.currentText()])
        if setsData != None:
            self.fillComboKeys(self.setCombo, setsData)
            self.setCombo.setToolTip(tr("page.all_sets.setCombo.tooltip", [self.setCombo.count()]))
        else:
            self.clearResults()

    def handleSetCombo(self):
        self.updateSet()

    def handleIVBox(self):
        self.updateSet()

    def handleItemCheck(self):
        self.updateSet()

    def updateSet(self):
        self.clipboardButton.setText(tr("page.all_sets.clipboardButton"))
        self.currentSet = data.digForData(self.getSets(), [self.pokeCombo.currentText(), int(self.setCombo.currentText())]) if self.setCombo.currentText().isdecimal() else None
        if self.currentSet != None:
            hideItem = self.itemCheck.isChecked()
            string = self.currentSet.getShowdownFormat(self.ivBox.value(), hideItem = hideItem)
            # speed and modifiers
            speed = self.currentSet.getSpeed(self.ivBox.value())
            string += "\n" + tr("page.sets.result.speed", [speed]) + "\n"
            if not hideItem:
                if self.currentSet.item == "Choice Scarf":
                    speed = math.floor(speed * 1.5)
                    string += tr("page.sets.result.speed.item", ["Choice Scarf", speed]) + "\n"
                if self.currentSet.item == "Iron Ball":
                    speed = math.floor(speed * 0.5)
                    string += tr("page.sets.result.speed.item", ["Iron Ball", speed]) + "\n"
            if "Slow Start" in self.currentSet.species.abilities:
                speed = math.floor(speed * 0.5)
                string += tr("page.sets.result.speed.ability", ["Slow Start", speed]) + "\n"
            if "Unburden" in self.currentSet.species.abilities:
                speed = math.floor(speed * 2.0)
                string += tr("page.sets.result.speed.ability", ["Unburden", speed]) + "\n"
            # it's important to say specifically what the possible abilities are because some pokemon have gotten new abilities in new games
            if not self.currentSet.species.hasOneAbility():
                string += "\n" + tr("page.sets.result.abilities", self.currentSet.species.abilities) + "\n"
            self.output.setText(string)
            self.clipboardButton.setEnabled(True)
            self.pokeCombo.setToolTip(str(self.currentSet.species))
        else:
            self.clearResults()

    def clearResults(self):
        self.output.setText(tr("page.all_sets.empty_results"))
        self.clipboardButton.setEnabled(False)
        self.pokeCombo.setToolTip("")
        self.setCombo.setToolTip("")

    def copyToClipboard(self):
        if self.currentSet != None:
            QGuiApplication.clipboard().setText(self.currentSet.getShowdownFormat(self.ivBox.value(), hideItem = self.itemCheck.isChecked()))
            self.clipboardButton.setText(tr("page.all_sets.clipboardButton.copied"))

# browse all sets
class BrowseAllSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, setProvider):
        super().__init__(parent)

        self.setProvider = setProvider
        self.setsA = data.setsAlphaSorted(self.setProvider.sets)
        self.setsD = data.setsDexSorted(self.setProvider.sets)
        self.setupIVBox(self.setProvider)

        self.pokeLabel.setToolTip(tr("page.all_sets.pokemon.tooltip"))
        self.ivLabel.setToolTip(tr("page.all_sets.ivs.tooltip"))

        # set up initial state
        self.fillComboKeys(self.pokeCombo, self.getSets())

# browse sets by trainer
class BrowseTrainerSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, battlenumToSetProviders):
        super().__init__(parent)

        self.battlenumToSetProviders = battlenumToSetProviders

        trainerSelect = QHBoxLayout()
        self.layout().insertLayout(0, trainerSelect)

        # battle number combo box
        self.battlenumLabel = QLabel(tr("page.all_sets_by_trainer.battle_number"))
        self.battlenumLabel.setToolTip(tr("page.all_sets_by_trainer.battle_number.tooltip"))
        self.battlenumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.battlenumLabel)
        self.battlenumCombo = self.addComboBox(self.handleBattlenumCombo, trainerSelect)

        # trainer class & name combo boxes
        self.trainerLabel = QLabel(tr("page.all_sets_by_trainer.trainer"))
        self.trainerLabel.setToolTip(tr("page.all_sets_by_trainer.trainer.tooltip"))
        self.trainerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.trainerLabel)
        self.tclassCombo = self.addComboBox(self.handleTClassCombo, trainerSelect)
        self.tnameCombo = self.addComboBox(self.handleTNameCombo, trainerSelect)

        self.pokeLabel.setToolTip(tr("page.all_sets_by_trainer.pokemon.tooltip"))
        self.ivLabel.setToolTip(tr("page.all_sets_by_trainer.ivs.tooltip"))

        # set up initial state
        self.fillComboKeys(self.battlenumCombo, self.bTSP())

    def bTSP(self):
        return self.battlenumToSetProviders

    # when the battle number combo box updates, tells the trainer class combo box to update
    def handleBattlenumCombo(self):
        tclassData = data.digForData(self.bTSP(), [self.battlenumCombo.currentText()])
        if tclassData != None:
            self.fillComboKeys(self.tclassCombo, tclassData)
        else:
            self.clearTrainerResults()

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self):
        tnameData = data.digForData(self.bTSP(), [self.battlenumCombo.currentText(), self.tclassCombo.currentText()])
        if tnameData != None:
            self.fillComboKeys(self.tnameCombo, tnameData)
        else:
            self.clearTrainerResults()

    def handleTNameCombo(self):
        self.updateTrainer()

    def updateTrainer(self):
        currentProvider = data.digForData(self.bTSP(), [self.battlenumCombo.currentText(), self.tclassCombo.currentText(), self.tnameCombo.currentText()])
        if currentProvider != None:
            self.setsA = data.setsAlphaSorted(currentProvider.sets)
            self.setsD = data.setsDexSorted(currentProvider.sets)
            # when the trainer selection updates, tells the species combo box to update
            self.fillComboKeys(self.pokeCombo, self.getSets())
            self.setupIVBox(currentProvider)
            self.battlenumCombo.setToolTip(self.battlenumCombo.currentText())
            self.tclassCombo.setToolTip(self.tclassCombo.currentText())
            self.tnameCombo.setToolTip(self.tnameCombo.currentText())
        else:
            self.clearTrainerResults()

    def clearTrainerResults(self):
        self.fillComboKeys(self.pokeCombo, {})
        self.battlenumCombo.setToolTip("")
        self.tclassCombo.setToolTip("")
        self.tnameCombo.setToolTip("")
