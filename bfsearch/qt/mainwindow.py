# qt


import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTabWidget, QMainWindow, QToolBar, QMessageBox, QLabel, QTextEdit, QPushButton, QInputDialog
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

from bfsearch import core
from bfsearch import data
from bfsearch.qt import browse
from bfsearch import translate
from bfsearch.translate import tr


# code for recreating the main window. if the application exits with this code, the main window will be recreated.
RECREATE_CODE = 0x16119

def launch():
    app = QApplication(sys.argv)
    currentCode = RECREATE_CODE
    while currentCode == RECREATE_CODE:
        window = Window()
        window.show()
        currentCode = app.exec()
        window.hide()
        del window
    sys.exit()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = data.DataHolder()

        self.resize(750, 450)
        self.setWindowTitle("BFSearch")
        self.setWindowIcon(QIcon("gui/icon.png"))
        self.setCentralWidget(QTabWidget(self))

        # toolbar buttons #todo: icons
        self.toolBar = QToolBar(tr("toolbar.name"))
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolBar)
        # language
        self.addToolBarButton(tr("toolbar.button.language.name"), tr("toolbar.button.language.tooltip"), self.language)
        # about
        self.addToolBarButton(tr("toolbar.button.about.name"), tr("toolbar.button.about.tooltip"), self.about)
        # about qt
        self.addToolBarButton(tr("toolbar.button.about_qt.name"), tr("toolbar.button.about_qt.tooltip"), QApplication.aboutQt)  # how does this get translated?

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

    def addToolBarButton(self, name, tooltip, connect):
        toolBarButton = QAction(name, self)
        toolBarButton.setToolTip(tooltip)
        toolBarButton.triggered.connect(connect)
        self.toolBar.addAction(toolBarButton)

    def build(self):
        self.buildButton.setDisabled(True)

        # clear other tabs
        self.centralWidget().clear()
        self.centralWidget().addTab(self.welcomePage, tr("page.welcome.name"))

        self.textLog.setText(tr("page.welcome.status.parsing"))
        # force updates the text log
        self.textLog.repaint()

        # builds data
        result = self.data.fillerup()
        if self.data.isEmpty:
            self.textLog.setText(tr("page.welcome.status.error", [result]))
        else:
            self.textLog.setText(tr("page.welcome.status.done"))
            self.addOtherPages()

        self.buildButton.setDisabled(False)

    def addOtherPages(self):
        self.browseSetsPage = browse.BrowseAllSetsPage(self, core.SetProvider(0, 31, [], self.data.sets))
        self.centralWidget().addTab(self.browseSetsPage, QIcon("gui/pokemon.png"), tr("page.all_sets.name"))
        self.centralWidget().setTabToolTip(1, tr("page.all_sets.tooltip"))

        self.browseTrainerSetsPage = browse.BrowseTrainerSetsPage(self, data.battlenumToGroupedSetProviders(self.data.trainers))
        self.centralWidget().addTab(self.browseTrainerSetsPage, QIcon("gui/trainers.png"), tr("page.all_sets_by_trainer.name"))
        self.centralWidget().setTabToolTip(2, tr("page.all_sets_by_trainer.tooltip"))

    def language(self):
        prettyDict = translate.prettyLangsDict()
        note = tr("toolbar.button.language.note")
        if len(prettyDict) <= 1:
            note +="\n" + tr("toolbar.button.language.note.single")
        prettyLang, ok = QInputDialog.getItem(self, tr("toolbar.button.language.tooltip"), note, prettyDict.keys(), translate.currentLangIndex(), False)
        if ok and prettyLang:
            lang = prettyDict[prettyLang]
            if lang != translate.currentLang:
                translate.currentLang = lang
                # also put it in a .cfg?
                QApplication.exit(RECREATE_CODE)

    def about(self):
        QMessageBox.about(self, tr("toolbar.button.about.name"), tr("toolbar.button.about.about"))


def commaList(alist):
    if len(alist) > 0:
        string = str(alist[0])
        if len(alist) > 1:
            for i in range(1, len(alist)):
                string += ", " + str(alist[i])
        return string
    else:
        return ""
