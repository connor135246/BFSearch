# qt


import json
import sys
import math

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QTabWidget, QMainWindow, QDockWidget, QToolBar, QMessageBox, QLabel, QComboBox, QTextEdit, QSizePolicy, QPushButton, QSpinBox, QCheckBox
from PySide6.QtGui import QIcon, QAction, QActionGroup, QGuiApplication
from PySide6.QtCore import Qt, QSize


from bfsearch import core
from bfsearch import data
from bfsearch.translate import getTranslation



def launch():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


# translate
def tr(key, args = []):
    return getTranslation(key).format(*args)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = data.DataHolder()
    
        self.resize(750, 450)
        self.setWindowTitle("BFSearch")
        self.setWindowIcon(QIcon("gui/icon.png"))
        self.setCentralWidget(QTabWidget(self))

        # toolbar
        self.toolbar = QToolBar(tr("toolbar.name"))
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)
        # about
        aboutAct = QAction(tr("toolbarbutton.about.name"), self)
        aboutAct.setStatusTip(tr("toolbarbutton.about.tooltip"))
        aboutAct.triggered.connect(self.about)
        self.toolbar.addAction(aboutAct)
        # about qt
        aboutQtAct = QAction(tr("toolbarbutton.about_qt.name"), self)
        aboutQtAct.setStatusTip(tr("toolbarbutton.about_qt.tooltip"))
        aboutQtAct.triggered.connect(QApplication.aboutQt) # how does this get translated?
        self.toolbar.addAction(aboutQtAct)

        # start page
        self.welcomePage = QWidget(self)
        self.welcomePage.setLayout(QVBoxLayout())
        self.buildButton = QPushButton(tr("page.welcome.buildButton"))
        self.buildButton.clicked.connect(self.build)
        self.textLog = QTextEdit()
        self.textLog.setReadOnly(True)
        self.textLog.setText(tr("page.welcome.status.ready"))
        self.welcomePage.layout().addWidget(QLabel(tr("page.welcome.welcome")))
        self.welcomePage.layout().addWidget(self.buildButton)
        self.welcomePage.layout().addWidget(self.textLog)
        self.centralWidget().addTab(self.welcomePage, tr("page.welcome.name"))

    def build(self):
        # clear other tabs
        self.centralWidget().clear()
        self.centralWidget().addTab(self.welcomePage, tr("page.welcome.name"))
        
        self.buildButton.setDisabled(True)

        self.textLog.setText(tr("page.welcome.status.parsing"))
        # force updates the text log
        self.textLog.repaint()

        # builds data
        result = self.data.fillerup()
        if self.data.isEmpty:
            self.textLog.setText(tr("page.welcome.status.error", [result]))
        else:
            self.textLog.setText(tr("page.welcome.status.done"))
            self.addPages()

        self.buildButton.setDisabled(False)

    def addPages(self):
        self.browseSetsPage = BrowseAllSetsPage(self, core.SetProvider(0, 31, [], self.data.sets))
        self.centralWidget().addTab(self.browseSetsPage, QIcon("gui/pokemon.png"), tr("page.all_sets.name"))
        self.centralWidget().setTabToolTip(1, tr("page.all_sets.tooltip"))
        
        self.browseTrainerSetsPage = BrowseTrainerSetsPage(self, data.battlenumToGroupedSetProviders(self.data.trainers))
        self.centralWidget().addTab(self.browseTrainerSetsPage, QIcon("gui/trainers.png"), tr("page.all_sets_by_trainer.name"))
        self.centralWidget().setTabToolTip(2, tr("page.all_sets_by_trainer.tooltip"))

    def about(self):
        QMessageBox.about(self, tr("toolbarbutton.about.name"), tr("toolbarbutton.about.about"))

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

        # species combo box
        self.pokeCombo = QComboBox()
        self.pokeCombo.currentTextChanged.connect(self.handlePokeCombo)
        self.pokeLabel = QLabel(tr("page.all_sets.pokemon"))
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
        self.ivLabel = QLabel(tr("page.all_sets.ivs"))
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
        if self.pokeCombo.currentText() in self.getSets().keys():
            self.fillComboKeys(self.setCombo, self.getSets()[self.pokeCombo.currentText()])
            self.setCombo.setToolTip(tr("page.all_sets.setCombo.tooltip", [self.setCombo.count()]))
        else:
            self.updateSet()

    def handleSetCombo(self):
        self.updateSet()

    def handleIVBox(self):
        self.updateSet()

    def setupIVBox(self, setProvider):
        self.ivBox.setRange(setProvider.minIV, setProvider.maxIV)
        if self.ivBox.minimum() == self.ivBox.maximum():
            self.ivBox.setToolTip(tr("page.all_sets.ivBox.tooltip.fixed"))
            self.ivBox.setEnabled(False)
        else:
            self.ivBox.setToolTip(tr("page.all_sets.ivBox.tooltip.range", [self.ivBox.minimum(), self.ivBox.maximum()]))
            self.ivBox.setEnabled(True)

    def handleItemCheck(self):
        self.updateSet()

    def updateSet(self):
        self.clipboardButton.setText(tr("page.all_sets.clipboardButton"))
        if self.pokeCombo.currentText() in self.getSets().keys():
            if self.setCombo.currentText().isdecimal() and (int(self.setCombo.currentText()) in self.getSets()[self.pokeCombo.currentText()].keys()):
                self.currentSet = self.getSets()[self.pokeCombo.currentText()][int(self.setCombo.currentText())]
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
                return
        self.currentSet = None
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

        self.setsA = data.setsAlphaSorted(self.getSetProvider().sets)
        self.setsD = data.setsDexSorted(self.getSetProvider().sets)

        self.setupIVBox(self.getSetProvider())

        self.pokeLabel.setToolTip(tr("page.all_sets.pokemon.tooltip"))
        self.ivLabel.setToolTip(tr("page.all_sets.ivs.tooltip"))

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
        self.battlenumLabel = QLabel(tr("page.all_sets_by_trainer.battle_number"))
        self.battlenumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.battlenumLabel)
        trainerSelect.addWidget(self.battlenumCombo)

        # trainer class combo box
        self.tclassCombo = QComboBox()
        self.tclassCombo.currentTextChanged.connect(self.handleTClassCombo)
        self.trainerLabel = QLabel(tr("page.all_sets_by_trainer.trainer"))
        self.trainerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainerSelect.addWidget(self.trainerLabel)
        trainerSelect.addWidget(self.tclassCombo)

        # trainer name combo box
        self.tnameCombo = QComboBox()
        self.tnameCombo.currentTextChanged.connect(self.handleTNameCombo)
        trainerSelect.addWidget(self.tnameCombo)

        self.battlenumLabel.setToolTip(tr("page.all_sets_by_trainer.battle_number.tooltip"))
        self.trainerLabel.setToolTip(tr("page.all_sets_by_trainer.trainer.tooltip"))

        self.pokeLabel.setToolTip(tr("page.all_sets_by_trainer.pokemon.tooltip"))
        self.ivLabel.setToolTip(tr("page.all_sets_by_trainer.ivs.tooltip"))

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


def commaList(alist):
    if len(alist) > 0:
        string = str(alist[0])
        if len(alist) > 1:
            for i in range(1, len(alist)):
                string += ", " + str(alist[i])
        return string
    else:
        return ""

