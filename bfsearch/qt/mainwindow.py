# qt


import sys, logging

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTabWidget, QMainWindow, QToolBar, QMessageBox, QLabel, QTextEdit, QPushButton, QInputDialog, QStyle
from PySide6.QtGui import QIcon, QAction, QGuiApplication
from PySide6.QtCore import Qt

from bfsearch import data, translate, settings
from bfsearch.translate import tr
from bfsearch.qt import browse, search, browsehall


# code for recreating the main window. if the application exits with this code, the main window will be recreated.
RECREATE_CODE = 0x16111

def launch():
    app = QApplication(sys.argv)
    logging.info("Starting!")
    currentCode = RECREATE_CODE
    while currentCode == RECREATE_CODE:
        window = Window()
        window.show()
        currentCode = app.exec()
        window.hide()
        del window
    logging.info("Stopping!")
    sys.exit()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = data.DataHolder()

        self.resize(750, 623)
        self.setWindowTitle("BFSearch")
        self.setWindowIcon(QIcon("gui/icon.png"))
        self.setCentralWidget(QTabWidget(self))

        # toolbar buttons
        self.toolBar = QToolBar(tr("toolbar.name"))
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolBar)
        # language
        self.addToolBarButton(QIcon("gui/language.png"), tr("toolbar.button.language.name"), tr("toolbar.button.language.tooltip"), self.language)
        # about
        self.addToolBarButton(QIcon("gui/about.png"), tr("toolbar.button.about.name"), tr("toolbar.button.about.tooltip"), self.about)
        # about qt
        self.addToolBarButton(self.style().standardIcon(QStyle.SP_TitleBarMenuButton), tr("toolbar.button.about_qt.name"), tr("toolbar.button.about_qt.tooltip"), QApplication.aboutQt)  # how does this get translated?

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

    def addToolBarButton(self, icon, name, tooltip, connect):
        toolBarButton = QAction(icon, name, self)
        toolBarButton.setToolTip(tooltip)
        toolBarButton.triggered.connect(connect)
        self.toolBar.addAction(toolBarButton)

    def build(self):
        self.buildButton.setDisabled(True)

        # clear other tabs
        self.centralWidget().clear()
        self.centralWidget().addTab(self.welcomePage, tr("page.welcome.name"))

        self.textLog.setText(tr("page.welcome.status.parsing"))
        self.textLog.repaint()

        # builds data
        result = self.data.fillerup()
        if self.data.isEmpty:
            self.textLog.setText(tr("page.welcome.status.error", result))
        else:
            self.textLog.setText(tr("page.welcome.status.building"))
            self.textLog.repaint()
            self.addOtherPages()
            self.textLog.setText(tr("page.welcome.status.done"))

        self.buildButton.setDisabled(False)

    def addOtherPages(self):
        self.browseSetsPage = browse.BrowseAllSetsPage(self, data.genericSetProvider(self.data.sets))
        self.centralWidget().addTab(self.browseSetsPage, QIcon("gui/pokemon.png"), tr("page.all_sets.name"))
        self.centralWidget().setTabToolTip(1, tr("page.all_sets.tooltip"))

        self.browseTrainerSetsPage = browse.BrowseTrainerSetsPage(self, data.battlenumToGroupedSetProviders(self.data.trainers))
        self.centralWidget().addTab(self.browseTrainerSetsPage, QIcon("gui/trainers.png"), tr("page.all_sets_by_trainer.name"))
        self.centralWidget().setTabToolTip(2, tr("page.all_sets_by_trainer.tooltip"))

        self.searchPage = search.SearchPage(self, self.data)
        self.centralWidget().addTab(self.searchPage, QIcon("gui/search.png"), tr("page.search.name"))
        self.centralWidget().setTabToolTip(3, tr("page.search.tooltip"))

        self.browseHallSetsPage = browsehall.BrowseAllHallSetsPage(self, data.genericSetProvider(self.data.hall_sets))
        self.centralWidget().addTab(self.browseHallSetsPage, QIcon("gui/hallpokemon.png"), tr("page.hall_sets.name"))
        self.centralWidget().setTabToolTip(4, tr("page.hall_sets.tooltip"))

        self.calcHallSetsPage = browsehall.CalcHallSetsPage(self, data.typeToRankToHallSets(self.data.hall_sets), data.hallSetGroupToHallSets(self.data.hall_sets))
        self.centralWidget().addTab(self.calcHallSetsPage, QIcon("gui/hallcalc.png"), tr("page.hall_calc.name"))
        self.centralWidget().setTabToolTip(5, tr("page.hall_calc.tooltip"))

        logging.info("Built data!")

    def language(self):
        prettyDict = translate.prettyLangsDict()
        note = tr("toolbar.button.language.note")
        if len(prettyDict) <= 1:
            note += "\n" + tr("toolbar.button.language.note.single")
        prettyLang, ok = QInputDialog.getItem(self, tr("toolbar.button.language.tooltip"), note, prettyDict.keys(), translate.currentLangIndex(), False)
        if ok and prettyLang:
            lang = prettyDict[prettyLang]
            if lang != translate.currentLang:
                translate.currentLang = lang
                logging.info("Changed language!")
                settings.settings[translate.settingsKey] = lang
                settings.save()
                logging.info("Restarting!")
                QApplication.exit(RECREATE_CODE)

    def about(self):
        about = QMessageBox(QMessageBox.Information, tr("toolbar.button.about.name"), tr("toolbar.button.about.about"), buttons = QMessageBox.StandardButton.Ok, parent = self)
        linkButton = about.addButton(tr("toolbar.button.about.linkButton"), QMessageBox.ActionRole)
        about.setEscapeButton(QMessageBox.Ok)
        about.exec()
        if about.clickedButton() == linkButton:
            QGuiApplication.clipboard().setText("https://calc.pokemonshowdown.com/index.html?gen=4")


def commaList(alist):
    if len(alist) > 0:
        string = str(alist[0])
        if len(alist) > 1:
            for i in range(1, len(alist)):
                string += ", " + str(alist[i])
        return string
    else:
        return ""
