# browse


import math

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QTextEdit, QPushButton, QSpinBox, QCheckBox, QGroupBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt

from bfsearch import data
from bfsearch.translate import tr


def getSetResultString(the_set, iv, hideItem, level = 50):
    string = the_set.getShowdownFormat(iv, level = level, hideItem = hideItem)
    speed = the_set.getSpeed(iv, level = level)
    string += "\n" + tr("page.generic.result.speed", speed)
    if not hideItem:
        if the_set.item == "Choice Scarf":
            speed = math.floor(speed * 1.5)
            string += "\n" + tr("page.generic.result.speed.item", "Choice Scarf", speed)
        if the_set.item == "Iron Ball":
            speed = math.floor(speed * 0.5)
            string += "\n" + tr("page.generic.result.speed.item", "Iron Ball", speed)
    if "Slow Start" in the_set.species.abilities:
        string += "\n" + tr("page.generic.result.speed.ability", "Slow Start", math.floor(speed * 0.5))
    if "Unburden" in the_set.species.abilities:
        string += "\n" + tr("page.generic.result.speed.ability", "Unburden", math.floor(speed * 2.0))
    # it's important to say specifically what the possible abilities are because some pokemon have gotten new abilities in new games
    if not the_set.species.hasOneAbility():
        string += "\n\n" + tr("page.generic.result.abilities", *the_set.species.abilities)
    #string += "\nID: " + str(the_set.sid) + "\n"
    #string += "Set Group: " + the_set.setgroup.name + "\n"
    #string += "Types: " + str(the_set.species.types) + "\n"
    return string


# base class for functional pages
# contains an alpha/dex sortable, an output, and a copy to clipboard button with item check
class SharedPageElements(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # alphabetically organized sets
        self.sortedAlpha = None
        # dex number organized sets
        self.sortedDex = None
        # sort toggle button
        self.sortToggle = QPushButton("")
        self.alpha = True
        self.setSortToggleText()
        self.sortToggle.clicked.connect(self.toggleSorting)
        self.sortToggle.setToolTip(tr("page.generic.sortToggle.tooltip"))

        # output
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # clipboard options
        self.clipboardOptions = QHBoxLayout()
        # copy to clipboard button
        self.clipboardButton = QPushButton("")
        self.clipboardButton.clicked.connect(self.copyToClipboard)
        self.clipboardOptions.addWidget(self.clipboardButton, stretch = 1)
        # current set (for copy to clipboard)
        self.currentSet = None
        # hide held items checkbox
        self.itemCheck = QCheckBox(tr("page.generic.itemCheck"))
        self.itemCheck.stateChanged.connect(self.handleItemCheck)
        self.clipboardOptions.addWidget(self.itemCheck)
        self.itemCheck.setToolTip(tr("page.generic.itemCheck.tooltip"))

    ### override and call super to add functionality
    def toggleSorting(self):
        self.alpha = not self.alpha
        self.setSortToggleText()

    def setSortToggleText(self):
        if self.alpha:
            self.sortToggle.setText(tr("page.generic.sortToggle.alpha"))
        else:
            self.sortToggle.setText(tr("page.generic.sortToggle.dex"))

    def getSorted(self):
        return self.getSortedAlpha() if self.alpha else self.getSortedDex()

    def getSortedAlpha(self):
        return self.sortedAlpha

    def getSortedDex(self):
        return self.sortedDex

    def handleItemCheck(self):
        self.updateSet()

    ### override and call super to add functionality
    def updateSet(self):
        self.clipboardButton.setText(tr("page.generic.clipboardButton"))

    ### override to add functionality
    def getIV(self):
        return 31

    def copyToClipboard(self):
        if self.currentSet is not None:
            QGuiApplication.clipboard().setText(self.currentSet.getShowdownFormat(self.getIV(), hideItem = self.itemCheck.isChecked()))
            self.clipboardButton.setText(tr("page.generic.clipboardButton.copied"))


# base page for single set browsing
class BrowseSetsPageBase(SharedPageElements):
    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QVBoxLayout(self))

        mainBox = QGroupBox("")
        self.mainLayout = QVBoxLayout(mainBox)
        mainBox.setLayout(self.mainLayout)
        self.layout().addWidget(mainBox)

        # sort toggle
        self.mainLayout.addWidget(self.sortToggle)

        ## set selector
        setSelect = QHBoxLayout()
        self.mainLayout.addLayout(setSelect)

        # species & set combo boxes
        self.pokeLabel = QLabel(tr("page.generic.pokemon"))
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
        self.mainLayout.addWidget(self.output)

        # clipboard options
        self.mainLayout.addLayout(self.clipboardOptions)

        # set up initial state
        self.updateSet()

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

    # when the species combo box updates, tells the set combo box to update
    def handlePokeCombo(self):
        setsData = data.digForData(self.getSorted(), [self.pokeCombo.currentText()])
        if setsData is not None:
            self.fillComboKeys(self.setCombo, setsData)
            if self.setCombo.count() == 1:
                self.setCombo.setToolTip(tr("page.all_sets.setCombo.tooltip.singular", self.setCombo.count()))
            else:
                self.setCombo.setToolTip(tr("page.all_sets.setCombo.tooltip.plural", self.setCombo.count()))
        else:
            self.clearResults()

    def handleSetCombo(self):
        self.updateSet()

    def handleIVBox(self):
        self.updateSet()

    def updateSet(self):
        super().updateSet()
        self.currentSet = data.digForData(self.getSorted(), [self.pokeCombo.currentText(), int(self.setCombo.currentText())]) if self.setCombo.currentText().isdecimal() else None
        if self.currentSet is not None:
            self.output.setText(getSetResultString(self.currentSet, self.ivBox.value(), self.itemCheck.isChecked()))
            self.clipboardButton.setEnabled(True)
            self.pokeCombo.setToolTip(str(self.currentSet.species))
        else:
            self.clearResults()

    def clearResults(self):
        self.output.setText(tr("page.all_sets.empty_results"))
        self.clipboardButton.setEnabled(False)
        self.pokeCombo.setToolTip("")
        self.setCombo.setToolTip("")


# browse all sets
class BrowseAllSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, setProvider):
        super().__init__(parent)

        self.setProvider = setProvider
        self.sortedAlpha = data.setsAlphaSorted(self.setProvider.sets)
        self.sortedDex = data.setsDexSorted(self.setProvider.sets)
        self.setupIVBox(0, 31)

        self.layout().insertWidget(0, QLabel(tr("page.all_sets.info")))
        self.pokeLabel.setToolTip(tr("page.all_sets.pokemon.tooltip"))
        self.ivLabel.setToolTip(tr("page.all_sets.ivs.tooltip"))

        # set up initial state
        self.fillComboKeys(self.pokeCombo, self.getSorted())


# browse sets by trainer
class BrowseTrainerSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, battlenumToSetProviders):
        super().__init__(parent)

        self.battlenumToSetProviders = battlenumToSetProviders

        ## trainer selector
        trainerSelect = QHBoxLayout()
        self.mainLayout.insertLayout(0, trainerSelect)

        # battle number combo box
        self.battlenumLabel = QLabel(tr("page.generic.battle_number"))
        self.battlenumLabel.setToolTip(tr("page.all_sets_by_trainer.battle_number.tooltip"))
        self.battlenumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.battlenumLabel)
        self.battlenumCombo = self.addComboBox(self.handleBattlenumCombo, trainerSelect)

        # trainer class & name combo boxes
        self.trainerLabel = QLabel(tr("page.generic.trainer"))
        self.trainerLabel.setToolTip(tr("page.all_sets_by_trainer.trainer.tooltip"))
        self.trainerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.trainerLabel)
        self.tclassCombo = self.addComboBox(self.handleTClassCombo, trainerSelect)
        self.tnameCombo = self.addComboBox(self.handleTNameCombo, trainerSelect)

        self.layout().insertWidget(0, QLabel(tr("page.all_sets_by_trainer.info")))
        self.pokeLabel.setToolTip(tr("page.all_sets_by_trainer.pokemon.tooltip"))
        self.ivLabel.setToolTip(tr("page.all_sets_by_trainer.ivs.tooltip"))
        self.darachLabel = QLabel(tr("page.all_sets_by_trainer.darach"))
        self.mainLayout.addWidget(self.darachLabel)
        self.darachLabel.hide()

        # set up initial state
        self.fillComboKeys(self.battlenumCombo, self.bTSP())

    def bTSP(self):
        return self.battlenumToSetProviders

    # when the battle number combo box updates, tells the trainer class combo box to update
    def handleBattlenumCombo(self):
        tclassData = data.digForData(self.bTSP(), [self.battlenumCombo.currentText()])
        if tclassData is not None:
            self.fillComboKeys(self.tclassCombo, tclassData)
        else:
            self.clearTrainerResults()

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self):
        self.darachLabel.hide()
        tnameData = data.digForData(self.bTSP(), [self.battlenumCombo.currentText(), self.tclassCombo.currentText()])
        if tnameData is not None:
            self.fillComboKeys(self.tnameCombo, tnameData)
            # darach works differently from every other trainer.
            if "Castle Valet" in self.tclassCombo.currentText():
                self.darachLabel.show()
        else:
            self.clearTrainerResults()

    def handleTNameCombo(self):
        self.updateTrainer()

    def updateTrainer(self):
        currentProvider = data.digForData(self.bTSP(), [self.battlenumCombo.currentText(), self.tclassCombo.currentText(), self.tnameCombo.currentText()])
        if currentProvider is not None:
            self.sortedAlpha = data.setsAlphaSorted(currentProvider.sets)
            self.sortedDex = data.setsDexSorted(currentProvider.sets)
            # when the trainer selection updates, tells the species combo box to update
            self.fillComboKeys(self.pokeCombo, self.getSorted())
            self.setupIVBox(currentProvider.minIV, currentProvider.maxIV)
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
