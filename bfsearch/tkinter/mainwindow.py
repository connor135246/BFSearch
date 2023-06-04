# mainwindow


import sys, logging

from tkinter import *
from tkinter import ttk
from idlelib.tooltip import Hovertip

from bfsearch import data, translate, settings
from bfsearch.translate import tr
from bfsearch.tkinter import browse, search, browsehall, dialogs, helpdialogs, coverage


# code for recreating the main window. if CURRENT_CODE is this when the application exits code, the main window will be recreated.
RECREATE_CODE = 0x16241
# the current code
CURRENT_CODE = [RECREATE_CODE]

def launch():
    # todo: command line arguments? (insta build, language)
    logging.info("Starting!")
    CURRENT_CODE[0] = RECREATE_CODE
    while CURRENT_CODE[0] == RECREATE_CODE:
        CURRENT_CODE[0] = 0x1594
        window = Window()
        window.mainloop()
        del window
        if CURRENT_CODE[0] == RECREATE_CODE:
            logging.info("Restarting!")
    logging.info("Stopping!")
    sys.exit()

# for settings
windowKey = "window_size+pos"
maximizedKey = "window_maximized"

# the root window.
class Window(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.data = data.DataHolder()

        self.title("BFSearch (Beta)")
        self.bficon = PhotoImage(file = "gui/frontier.png")
        self.wm_iconphoto(True, self.bficon)

        defaultGeometry = "750x625+120+60"
        try:
            self.geometry(settings.settings.get(windowKey, defaultGeometry))
        except TclError:
            self.geometry(defaultGeometry)
        self.minsize(350, 350)

        if settings.settings.get(maximizedKey, False):
            self.state('zoomed')

        self.protocol('WM_DELETE_WINDOW', self.deleteWindow)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(column = 0, row = 0, sticky = (W, N, E, S))
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)

        self.tabs = ttk.Notebook(self.mainframe)
        self.tabs.enable_traversal()
        self.tabs.grid(column = 0, row = 0, sticky = (W, N, E, S))
        self.starticon = PhotoImage(file = "gui/icon.png")
        self.tabs.add(self.createStartPage(), text = tr("page.welcome.name"), image = self.starticon, compound = 'left')

        self.update_idletasks()
        # build!
        self.after_idle(Window.build, self)

    def createStartPage(self):
        startPage = ttk.Frame(self.tabs)
        startPage.columnconfigure(0, weight = 1)
        startPage.rowconfigure(2, weight = 1)
        startPage.grid(column = 0, row = 0, sticky = (W, N, E, S))

        welcome = ttk.Label(startPage, text = tr("page.welcome.welcome"), wraplength = 730)
        welcome.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)

        self.buildButton = ttk.Button(startPage, text = tr("page.welcome.buildButton"), command = self.build)
        self.buildButton.state(["disabled"])
        self.buildButton.grid(column = 0, row = 1, sticky = (W, E), padx = 5)

        self.textLog = Text(startPage, width = 1, height = 1, wrap = 'word', state = 'disabled')
        self.textLog.grid(column = 0, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.setLogText(tr("page.welcome.status.ready"))

        self.toolbar = Toolbar(startPage)
        self.toolbar.grid(column = 0, row = 3, sticky = (W, N, E, S))

        return startPage

    def setLogText(self, text):
        self.textLog['state'] = 'normal'
        self.textLog.delete('1.0', 'end')
        self.textLog.insert('end', text)
        self.textLog['state'] = 'disabled'

    def deleteWindow(self):
        isMaximized = self.state() == 'zoomed'
        settings.settings[maximizedKey] = isMaximized
        if isMaximized:
            self.state('normal')
            self.update_idletasks()
        settings.settings[windowKey] = self.geometry()
        settings.save()
        self.quit()

    def build(self):
        self.buildButton.state(["disabled"])

        # clear other tabs
        for _ in range(1, len(self.tabs.tabs())):
            self.tabs.forget(1)

        # parses and builds data
        self.setLogText(tr("page.welcome.status.parsing"))
        self.update_idletasks()
        result = self.data.fillerup()
        if self.data.isEmpty:
            self.setLogText(tr("page.welcome.status.error", result))
        else:
            self.setLogText(tr("page.welcome.status.building"))
            self.update_idletasks()
            self.addOtherPages()
            self.setLogText(tr("page.welcome.status.done"))

        self.buildButton.state(["!disabled"])

    def addOtherPages(self):

        self.nonhallTabs = ttk.Notebook(self.tabs)
        self.nonhallTabs.enable_traversal()
        self.bfnh = PhotoImage(file = "gui/bfnh.png")
        self.tabs.add(self.nonhallTabs, text = tr("page.nonhall.name"), image = self.bfnh, compound = 'left')
        #tr("page.nonhall.tooltip")

        self.browseSetsPage = browse.BrowseAllSetsPage(self.nonhallTabs, data.genericSetProvider(self.data.sets))
        self.browseImage = PhotoImage(file = "gui/pokemon.png")
        self.nonhallTabs.add(self.browseSetsPage, text = tr("page.all_sets.name"), image = self.browseImage, compound = 'left')
        #tr("page.all_sets.tooltip")

        self.browseTrainerSetsPage = browse.BrowseTrainerSetsPage(self.nonhallTabs, self.data.facilities)
        self.trainerImage = PhotoImage(file = "gui/trainers.png")
        self.nonhallTabs.add(self.browseTrainerSetsPage, text = tr("page.all_sets_by_trainer.name"), image = self.trainerImage, compound = 'left')
        #tr("page.all_sets_by_trainer.tooltip")

        self.searchPage = search.SearchPage(self.nonhallTabs, self.data)
        self.searchImage = PhotoImage(file = "gui/search.png")
        self.nonhallTabs.add(self.searchPage, text = tr("page.search.name"), image = self.searchImage, compound = 'left')
        #tr("page.search.tooltip")

        self.coveragePage = coverage.CoveragePage(self.nonhallTabs, self.data)
        self.coverageImage = PhotoImage(file = "gui/coverage.png")
        self.nonhallTabs.add(self.coveragePage, text = tr("page.coverage.name"), image = self.coverageImage, compound = 'left')
        #tr("page.coverage.tooltip")

        self.hallTabs = ttk.Notebook(self.tabs)
        self.hallTabs.enable_traversal()
        self.bfh = PhotoImage(file = "gui/bfh.png")
        self.tabs.add(self.hallTabs, text = tr("page.hall.name"), image = self.bfh, compound = 'left')
        #tr("page.hall.tooltip")

        self.browseHallSetsPage = browsehall.BrowseAllHallSetsPage(self.hallTabs, data.hallSetProvider(self.data.hall_sets))
        self.hallImage = PhotoImage(file = "gui/hallpokemon.png")
        self.hallTabs.add(self.browseHallSetsPage, text = tr("page.hall_sets.name"), image = self.hallImage, compound = 'left')
        #tr("page.hall_sets.tooltip")

        self.calcHallSetsPage = browsehall.CalcHallSetsPage(self.hallTabs, data.typeToRankToHallSets(self.data.hall_sets), data.hallSetGroupToHallSets(self.data.hall_sets))
        self.hallcalcImage = PhotoImage(file = "gui/hallcalc.png")
        self.hallTabs.add(self.calcHallSetsPage, text = tr("page.hall_calc.name"), image = self.hallcalcImage, compound = 'left')
        #tr("page.hall_calc.tooltip")

        self.hallSearchPage = search.HallSearchPage(self.hallTabs, self.data)
        self.hallSearchImage = PhotoImage(file = "gui/hallsearch.png")
        self.hallTabs.add(self.hallSearchPage, text = tr("page.hall_search.name"), image = self.hallSearchImage, compound = 'left')
        #tr("page.hall_search.tooltip")

        self.hallCoveragePage = coverage.HallCoveragePage(self.hallTabs, self.data)
        self.hallCoverageImage = PhotoImage(file = "gui/hallcoverage.png")
        self.hallTabs.add(self.hallCoveragePage, text = tr("page.hall_coverage.name"), image = self.hallCoverageImage, compound = 'left')
        #tr("page.hall_coverage.tooltip")

        logging.info("Built data!")


# the toolbar at the bottom of the window.
class Toolbar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding = (5, 5))

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.separator = ttk.Separator(self, orient = 'vertical')
        self.separator.pack(side = LEFT, fill = 'y', pady = 5)

        self.languageImage = PhotoImage(file = "gui/language.png")
        self.language = ttk.Button(self, text = tr("toolbar.button.language.name"), image = self.languageImage, compound = 'top', command = self.showLang, takefocus = 0)
        Hovertip(self.language, tr("toolbar.button.language.tooltip"), hover_delay = 1000)
        self.language.pack(side = LEFT, padx = 5)

        self.linksImage = PhotoImage(file = "gui/links.png")
        self.links = ttk.Button(self, text = tr("toolbar.button.links.name"), image = self.linksImage, compound = 'top', command = self.showLinks, takefocus = 0)
        Hovertip(self.links, tr("toolbar.button.links.tooltip"), hover_delay = 1000)
        self.links.pack(side = LEFT, padx = 5)

        self.helpImage = PhotoImage(file = "gui/help.png")
        self.help = ttk.Button(self, text = tr("toolbar.button.help.name"), image = self.helpImage, compound = 'top', command = self.showHelp, takefocus = 0)
        Hovertip(self.help, tr("toolbar.button.help.tooltip"), hover_delay = 1000)
        self.help.pack(side = LEFT, padx = 5)

    def showLinks(self):
        labels = [tr("toolbar.button.links.eisencalc"), tr("toolbar.button.links.smogon"), tr("toolbar.button.links.github")]
        links = ["https://eisencalc.com/", "https://www.smogon.com/forums/threads/4th-generation-battle-facilities-discussion-and-records.3663294/", "https://github.com/connor135246/BFSearch"]
        dialogs.LinksDialog(self._root(), tr("toolbar.button.links.name"), [tr("toolbar.button.ok")], tr("toolbar.button.links.links"), "gui/links.png", labels, links, tr("toolbar.button.links.copy"), tr("toolbar.button.links.copied")).show()

    def showLang(self):
        langs = translate.langs()
        note = tr("toolbar.button.language.note")
        if len(langs) <= 1:
            note += "\n" + tr("toolbar.button.language.note.single")
        langdialog = dialogs.ComboboxDialog(self._root(), tr("toolbar.button.language.name"), [tr("toolbar.button.ok"), tr("toolbar.button.cancel")], note, "gui/language.png", contents = langs, default = translate.currentLangIndex())
        pressed, combo = langdialog.show()
        if pressed == 0:
            if combo in langs:
                if combo != translate.currentLang:
                    translate.currentLang = combo
                    logging.info("Changed language!")
                    settings.settings[translate.settingsKey] = combo
                    settings.save()
                    CURRENT_CODE[0] = RECREATE_CODE
                    self._root().destroy()
            else:
                logging.warning(f"Invalid language selection: '{combo}'")

    def showHelp(self):
        helpdialogs.mainHelp(self._root())
