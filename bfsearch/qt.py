# qt


import json
import sys
import math

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QTabWidget, QMainWindow, QDockWidget, QToolBar, QMessageBox, QLabel, QComboBox, QTextEdit, QSizePolicy, QPushButton, QSpinBox, QCheckBox
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtCore import Qt, QSize
import pyperclip


from bfsearch import core
from bfsearch import data



def launch():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


# translate
def tr(string):
    return string

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = data.DataHolder()
    
        self.resize(750, 450)
        self.setWindowTitle("BFSearch")
        self.setWindowIcon(QIcon("gui/icon.png"))
        self.setCentralWidget(QTabWidget(self))

        # toolbar
        self.toolbar = QToolBar(tr("Buttons"))
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)
        # about
        aboutAct = QAction(tr("About"), self)
        aboutAct.setStatusTip(tr("Show this application's About box"))
        aboutAct.triggered.connect(self.about)
        self.toolbar.addAction(aboutAct)
        # about qt
        aboutQtAct = QAction(tr("About Qt"), self)
        aboutQtAct.setStatusTip(tr("Show the Qt library's About box"))
        aboutQtAct.triggered.connect(QApplication.aboutQt)
        self.toolbar.addAction(aboutQtAct)

        # start page
        self.welcomePage = QWidget(self)
        self.welcomePage.setLayout(QVBoxLayout())
        self.buildButton = QPushButton("Click to build data")
        self.buildButton.clicked.connect(self.build)
        self.textLog = QTextEdit()
        self.textLog.setReadOnly(True)
        self.textLog.setText("Ready.\n")
        self.welcomePage.layout().addWidget(QLabel(tr("Welcome. Click the button below to get started.\nAfter building data, additional tabs will appear on the top.")))
        self.welcomePage.layout().addWidget(self.buildButton)
        self.welcomePage.layout().addWidget(self.textLog)
        self.centralWidget().addTab(self.welcomePage, tr("Start Page"))

    def build(self):
        # clear other tabs
        self.centralWidget().clear()
        self.centralWidget().addTab(self.welcomePage, tr("Start Page"))
        
        self.buildButton.setDisabled(True)

        self.textLog.setText("Parsing...\n")
        # force updates the text log
        self.textLog.repaint()

        # builds data
        result = self.data.fillerup()
        if self.data.isEmpty:
            self.textLog.setText("Encountered an error while building data!\n    " + result + "\n\nPlease fix the error and try again.\n")
        else:
            self.textLog.setText("Data built successfully.\n")
            self.addPages()

        self.buildButton.setDisabled(False)

    def addPages(self):
        self.browseSetsPage = BrowseAllSetsPage(self, core.SetProvider(0, 31, [], self.data.sets))
        self.centralWidget().addTab(self.browseSetsPage, QIcon("gui/pokemon.png"), tr("Browse All Sets"))
        self.centralWidget().setTabToolTip(1, "Browse all possible Pokémon sets.")
        
        self.browseTrainerSetsPage = BrowseTrainerSetsPage(self, data.battlenumToGroupedSetProviders(self.data.trainers))
        self.centralWidget().addTab(self.browseTrainerSetsPage, QIcon("gui/trainers.png"), tr("Browse Sets by Trainer"))
        self.centralWidget().setTabToolTip(2, "Browse Pokémon sets organized by opposing trainers.")

    def about(self):
        QMessageBox.about(self, tr("About"), tr("This application allows you to search through the possible Pokémon that you can face in the Battle Tower in Platinum, HeartGold, and SoulSilver."))

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
        self.sortToggle.setToolTip("Toggle Pokémon sorting")

        setSelect = QHBoxLayout()
        self.layout().addLayout(setSelect)

        # species combo box
        self.pokeCombo = QComboBox()
        self.pokeCombo.currentTextChanged.connect(self.handlePokeCombo)
        self.pokeLabel = QLabel("Pokémon:")
        self.pokeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setSelect.addWidget(self.pokeLabel)
        setSelect.addWidget(self.pokeCombo)

        # set combo box
        self.setCombo = QComboBox()
        self.setCombo.currentTextChanged.connect(self.handleSetCombo)
        setSelect.addWidget(self.setCombo)

        # iv spin box
        self.ivBox = QSpinBox()
        self.ivBox.setRange(0, 31)
        self.ivBox.setValue(31)
        self.ivBox.valueChanged.connect(self.handleIVBox)
        self.ivLabel = QLabel("IVs:")
        self.ivLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setSelect.addWidget(self.ivLabel)
        setSelect.addWidget(self.ivBox)

        # output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout().addWidget(self.output)

        bottomOptions = QHBoxLayout()
        self.layout().addLayout(bottomOptions)

        # copy to clipboard button
        self.clipboardButton = QPushButton("Copy set to clipboard")
        self.clipboardButton.clicked.connect(self.copyToClipboard)
        bottomOptions.addWidget(self.clipboardButton, stretch = 1)
        # current set (for copy to clipboard)
        self.currentSet = None

        # hide held items checkbox
        self.itemCheck = QCheckBox("Hide held items")
        self.itemCheck.stateChanged.connect(self.handleItemCheck)
        bottomOptions.addWidget(self.itemCheck)
        self.itemCheck.setToolTip("Check this box if you're in the Battle Castle or Battle Arcade.\nPokémon in those facilities won't use the held items listed here.")

        # set up initial state
        self.updateSet()

    # sets the combo box data to the keys of the data
    def fillComboKeys(self, combo, data):
        combo.clear()
        for key in data.keys():
            combo.addItem(str(key))
        combo.setEnabled(combo.count() > 1)

    def toggleSorting(self):
        self.alpha = not self.alpha
        self.fillComboKeys(self.pokeCombo, self.getSets())
        self.setSortToggleText()

    def setSortToggleText(self):
        if self.alpha:
            self.sortToggle.setText("Sorting Pokémon alphabetically.")
        else:
            self.sortToggle.setText("Sorting Pokémon by Pokédex number.")

    def getSets(self):
        return self.getSetsAlpha() if self.alpha else self.getSetsDex()

    def getSetsAlpha(self):
        return self.setsA

    def getSetsDex(self):
        return self.setsD

    # when the species combo box updates, tells the set combo box to update
    def handlePokeCombo(self):
        if self.pokeCombo.currentText() in self.getSets().keys():
            self.fillComboKeys(self.setCombo, self.getSets()[self.pokeCombo.currentText()])
            self.setCombo.setToolTip(str(self.setCombo.count()) + " possible set(s)")
        else:
            self.updateSet()

    def handleSetCombo(self):
        self.updateSet()

    def handleIVBox(self):
        self.updateSet()

    def setupIVBox(self, setProvider):
        self.ivBox.setRange(setProvider.minIV, setProvider.maxIV)
        if self.ivBox.minimum() == self.ivBox.maximum():
            self.ivBox.setToolTip("The IV cannot be changed for these sets.")
            self.ivBox.setEnabled(False)
        else:
            self.ivBox.setToolTip(str(self.ivBox.minimum()) + " - " + str(self.ivBox.maximum()))
            self.ivBox.setEnabled(True)

    def handleItemCheck(self):
        self.updateSet()

    def updateSet(self):
        self.clipboardButton.setText("Copy set to clipboard")
        if self.pokeCombo.currentText() in self.getSets().keys():
            if self.setCombo.currentText().isdecimal() and (int(self.setCombo.currentText()) in self.getSets()[self.pokeCombo.currentText()].keys()):
                self.currentSet = self.getSets()[self.pokeCombo.currentText()][int(self.setCombo.currentText())]
                hideItem = self.itemCheck.isChecked()
                string = self.currentSet.getShowdownFormat(self.ivBox.value(), hideItem = hideItem)
                # speed and modifiers
                speed = self.currentSet.getSpeed(self.ivBox.value())
                string += f"\nSpeed (before items/modifiers/abilities): {speed}\n"
                if not hideItem:
                    if self.currentSet.item == "Choice Scarf":
                        speed = math.floor(speed * 1.5)
                        string += f"Speed (with Choice Scarf): {speed}\n"
                    if self.currentSet.item == "Iron Ball":
                        speed = math.floor(speed * 0.5)
                        string += f"Speed (with Iron Ball): {speed}\n"
                if "Slow Start" in self.currentSet.species.abilities:
                    speed = math.floor(speed * 0.5)
                    string += f"Speed (during Slow Start): {speed}\n"
                # it's important to say specifically what the possible abilities are because some pokemon have gotten new abilities in new games
                if not self.currentSet.species.hasOneAbility():
                    string += f"\nThis Pokemon's ability may be {commaList(self.currentSet.species.abilities)}.\n"
                self.output.setText(string)
                self.clipboardButton.setEnabled(True)
                self.pokeCombo.setToolTip(str(self.currentSet.species))
                return
        self.currentSet = None
        self.output.setText("Nothing doing!")
        self.clipboardButton.setEnabled(False)
        self.pokeCombo.setToolTip("")
        self.setCombo.setToolTip("")

    def copyToClipboard(self):
        pyperclip.copy(self.currentSet.getShowdownFormat(self.ivBox.value(), hideItem = self.itemCheck.isChecked()))
        self.clipboardButton.setText("Copied!")

# browse all sets
class BrowseAllSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, setProvider):
        super().__init__(parent)

        self.setProvider = setProvider

        self.setsA = data.setsAlphaSorted(self.getSetProvider().sets)
        self.setsD = data.setsDexSorted(self.getSetProvider().sets)

        self.setupIVBox(self.getSetProvider())

        self.pokeLabel.setToolTip("The number of possible sets depends on the Pokémon.\nMost Pokémon have 4 possible sets.\nWeaker Pokémon like mid-stage starters have 2 possible sets.\nVery weak Pokémon like first-stage starters have just 1 possible set.")
        self.ivLabel.setToolTip("Not all IVs are possible in the Battle Frontier.\nA Pokémon's IV depends on their trainer.")

        # set up initial state
        self.fillComboKeys(self.pokeCombo, self.getSets())

    def getSetProvider(self):
        return self.setProvider

# browse sets by trainer
class BrowseTrainerSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, battlenumToSetProviders):
        super().__init__(parent)

        self.battlenumToSetProviders = battlenumToSetProviders

        trainerSelect = QHBoxLayout()
        self.layout().insertLayout(0, trainerSelect)

        # battle number combo box
        self.battlenumCombo = QComboBox()
        self.battlenumCombo.currentTextChanged.connect(self.handleBattlenumCombo)
        self.battlenumLabel = QLabel("Battle Number:")
        self.battlenumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.battlenumLabel)
        trainerSelect.addWidget(self.battlenumCombo)

        # trainer class combo box
        self.tclassCombo = QComboBox()
        self.tclassCombo.currentTextChanged.connect(self.handleTClassCombo)
        self.trainerLabel = QLabel("Trainer:")
        self.trainerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.trainerLabel)
        trainerSelect.addWidget(self.tclassCombo)

        # trainer name combo box
        self.tnameCombo = QComboBox()
        self.tnameCombo.currentTextChanged.connect(self.handleTNameCombo)
        trainerSelect.addWidget(self.tnameCombo)

        self.battlenumLabel.setToolTip("Before battle 50, most trainers appear in two sets of rounds. For example, Idol Basia can appear in battles 1-6 or 7-13.\nThe 7th battle of each round will use a trainer that can appear in the next round. For example, Black Belt Mason can appear in battle 7, or in battles 8-13 or 15-20.\nOnce you reach battle 50, the trainer at the end of a round isn't any different from the others.")
        self.trainerLabel.setToolTip("Many trainers of the same class use the same sets of Pokémon.\nFor example: Youngsters Casimir, Erroll, and Jim are all the same.")

        self.pokeLabel.setToolTip("Before battle 50, all trainers use just one possible set for each of their Pokémon.\nOnce you reach battle 50, trainers may have multiple possible sets for each of their Pokémon.")
        self.ivLabel.setToolTip("A Pokémon's IV depends on their trainer.\nBefore battle 50, trainer IVs start at 3 and each round adds some trainers with the next multiple of 3. By the seventh round, you may face trainers with 21 IVs.\nOnce you reach battle 50, you'll usually be facing trainers with 31 IVs.\nAlso, Tower Tycoon Palmer has 31 IVs in both his battles.")

        # set up initial state
        self.fillComboKeys(self.battlenumCombo, self.getTripleDict())
        
    def getTripleDict(self):
        return self.battlenumToSetProviders

    # when the battle number combo box updates, tells the trainer class combo box to update
    def handleBattlenumCombo(self):
        if self.battlenumCombo.currentText() in self.getTripleDict().keys():
            self.fillComboKeys(self.tclassCombo, self.getTripleDict()[self.battlenumCombo.currentText()])
        else:
            self.updateTrainer()

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self):
        if self.battlenumCombo.currentText() in self.getTripleDict().keys():
            if self.tclassCombo.currentText() in self.getTripleDict()[self.battlenumCombo.currentText()].keys():
                self.fillComboKeys(self.tnameCombo, self.getTripleDict()[self.battlenumCombo.currentText()][self.tclassCombo.currentText()])
                return
        self.updateTrainer()

    def handleTNameCombo(self):
        self.updateTrainer()

    def updateTrainer(self):
        if self.battlenumCombo.currentText() in self.getTripleDict().keys():
            if self.tclassCombo.currentText() in self.getTripleDict()[self.battlenumCombo.currentText()].keys():
                if self.tnameCombo.currentText() in self.getTripleDict()[self.battlenumCombo.currentText()][self.tclassCombo.currentText()].keys():
                    this_provider = self.getTripleDict()[self.battlenumCombo.currentText()][self.tclassCombo.currentText()][self.tnameCombo.currentText()]
                    self.setsA = data.setsAlphaSorted(this_provider.sets)
                    self.setsD = data.setsDexSorted(this_provider.sets)
                    # when the trainer selection updates, tells the species combo box to update
                    self.fillComboKeys(self.pokeCombo, self.getSets())
                    self.setupIVBox(this_provider)
                    self.battlenumCombo.setToolTip(self.battlenumCombo.currentText())
                    self.tclassCombo.setToolTip(self.tclassCombo.currentText())
                    self.tnameCombo.setToolTip(self.tnameCombo.currentText())
                    return
        self.fillComboKeys(self.pokeCombo, {})
        self.battlenumCombo.setToolTip("")
        self.tclassCombo.setToolTip("")
        self.tnameCombo.setToolTip("")


def commaList(alist, useAnd = False):
    if len(alist) > 0:
        string = str(alist[0])
        if len(alist) > 1:
            for i in range(1, len(alist) - 1):
                string += ", " + str(alist[i])
            string += (" and " if useAnd else " or ") + str(alist[-1])
        return string
    else:
        return ""

def commaListSimple(alist):
    if len(alist) > 0:
        string = str(alist[0])
        if len(alist) > 1:
            for i in range(1, len(alist)):
                string += ", " + str(alist[i])
        return string
    else:
        return ""

