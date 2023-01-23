# qt


import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QTabWidget, QMainWindow, QDockWidget, QToolBar, QMessageBox, QLabel, QComboBox, QTextEdit, QSizePolicy, QPushButton, QSpinBox, QCheckBox
from PySide6.QtGui import QIcon, QAction, QActionGroup, QGuiApplication
from PySide6.QtCore import Qt, QSize

from bfsearch import core
from bfsearch import data
from bfsearch.qt import browse
from bfsearch.translate import tr



def launch():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


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
        # about
        self.addToolBarButton(tr("toolbar.button.about.name"), tr("toolbar.button.about.tooltip"), self.about)
        # about qt
        self.addToolBarButton(tr("toolbar.button.about_qt.name"), tr("toolbar.button.about_qt.tooltip"), QApplication.aboutQt) # how does this get translated?

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

