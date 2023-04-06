# mainwindow


import sys, logging

from tkinter import *
from tkinter import ttk
from idlelib.tooltip import Hovertip

from bfsearch import data, translate, settings
from bfsearch.translate import tr
from bfsearch.tkinter import browse, search, browsehall, dialogs



# code for recreating the main window. if CURRENT_CODE is this when the application exits code, the main window will be recreated.
RECREATE_CODE = 0x16111
# the current code
CURRENT_CODE = [RECREATE_CODE]

def launch():
    # todo: command line arguments? (insta build, language)
    logging.info("Starting!")
    CURRENT_CODE[0] = RECREATE_CODE
    while CURRENT_CODE[0] == RECREATE_CODE:
        CURRENT_CODE[0] = 0x1585
        window = Window()
        window.mainloop()
        del window
        if CURRENT_CODE[0] == RECREATE_CODE:
            logging.info("Restarting!")
    logging.info("Stopping!")
    sys.exit()


# the root window.
class Window(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.data = data.DataHolder()

        self.title("BFSearch")
        self.bficon = PhotoImage(file = "gui/frontier.png")
        self.wm_iconphoto(True, self.bficon)
        self.minsize(750, 633)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        #ttk.Style().theme_use("alt")

        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(column = 0, row = 0, sticky = (W, N, E, S))
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)

        self.tabs = ttk.Notebook(self.mainframe)
        self.tabs.enable_traversal()
        self.tabs.grid(column = 0, row = 0, sticky = (W, N, E, S))
        self.starticon = PhotoImage(file = "gui/icon.png")
        self.tabs.add(self.createStartPage(), text = tr("page.welcome.name"), image = self.starticon, compound = 'left')

        self.toolbar = Toolbar(self.mainframe)
        self.toolbar.grid(column = 0, row = 1, sticky = (W, N, E, S))

    def createStartPage(self):
        startPage = ttk.Frame(self.tabs)
        startPage.columnconfigure(0, weight = 1)
        startPage.rowconfigure(2, weight = 1)
        startPage.grid(column = 0, row = 0, sticky = (W, N, E, S))

        welcome = ttk.Label(startPage, text = tr("page.welcome.welcome"))
        welcome.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)

        self.buildButton = ttk.Button(startPage, text = tr("page.welcome.buildButton"), command = self.build)
        self.buildButton.grid(column = 0, row = 1, sticky = (W, E), padx = 5)

        self.textLog = Text(startPage, width = 1, height = 1, wrap = 'word', state = 'disabled')
        self.textLog.grid(column = 0, row = 2, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.setLogText(tr("page.welcome.status.ready"))

        return startPage

    def setLogText(self, text):
        self.textLog['state'] = 'normal'
        self.textLog.delete('1.0', 'end')
        self.textLog.insert('end', text)
        self.textLog['state'] = 'disabled'

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
        self.browseSetsPage = browse.BrowseAllSetsPage(self.tabs, data.genericSetProvider(self.data.sets))
        self.browseImage = PhotoImage(file = "gui/pokemon.png")
        self.tabs.add(self.browseSetsPage, text = tr("page.all_sets.name"), image = self.browseImage, compound = 'left')
        #tr("page.all_sets.tooltip")

        self.browseTrainerSetsPage = browse.BrowseTrainerSetsPage(self.tabs, self.data.facilities)
        self.trainerImage = PhotoImage(file = "gui/trainers.png")
        self.tabs.add(self.browseTrainerSetsPage, text = tr("page.all_sets_by_trainer.name"), image = self.trainerImage, compound = 'left')
        #tr("page.all_sets_by_trainer.tooltip")

        self.searchPage = search.SearchPage(self.tabs, self.data)
        self.searchImage = PhotoImage(file = "gui/search.png")
        self.tabs.add(self.searchPage, text = tr("page.search.name"), image = self.searchImage, compound = 'left')
        #tr("page.search.tooltip")

        self.browseHallSetsPage = browsehall.BrowseAllHallSetsPage(self.tabs, data.genericSetProvider(self.data.hall_sets))
        self.hallImage = PhotoImage(file = "gui/hallpokemon.png")
        self.tabs.add(self.browseHallSetsPage, text = tr("page.hall_sets.name"), image = self.hallImage, compound = 'left')
        #tr("page.hall_sets.tooltip")

        self.calcHallSetsPage = browsehall.CalcHallSetsPage(self.tabs, data.typeToRankToHallSets(self.data.hall_sets), data.hallSetGroupToHallSets(self.data.hall_sets))
        self.hallcalcImage = PhotoImage(file = "gui/hallcalc.png")
        self.tabs.add(self.calcHallSetsPage, text = tr("page.hall_calc.name"), image = self.hallcalcImage, compound = 'left')
        #tr("page.hall_calc.tooltip")

        logging.info("Built data!")


# the toolbar at the bottom of the window.
class Toolbar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth = 2, relief = 'solid', padding = (5, 10))

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.separator = ttk.Separator(self, orient = 'vertical')
        self.separator.pack(side = LEFT, fill = 'y', pady = 5)

        self.languageImage = PhotoImage(file = "gui/language.png")
        self.language = ttk.Button(self, text = tr("toolbar.button.language.name"), image = self.languageImage, compound = 'top', command = self.showLang, takefocus = 0)
        Hovertip(self.language, tr("toolbar.button.language.tooltip"), hover_delay = 1000)
        self.language.pack(side = LEFT, padx = 5)

        self.aboutImage = PhotoImage(file = "gui/about.png")
        self.about = ttk.Button(self, text = tr("toolbar.button.about.name"), image = self.aboutImage, compound = 'top', command = self.showAbout, takefocus = 0)
        Hovertip(self.about, tr("toolbar.button.about.tooltip"), hover_delay = 1000)
        self.about.pack(side = LEFT, padx = 5)

    def showAbout(self):
        aboutdialog = dialogs.InfoDialog(self._root(), tr("toolbar.button.about.name"), [tr("toolbar.button.ok"), tr("toolbar.button.about.linkButton")], tr("toolbar.button.about.about"), "gui/about.png")
        pressed = aboutdialog.show()
        if pressed == 1:
            self.clipboard_clear()
            self.clipboard_append("https://calc.pokemonshowdown.com/index.html?gen=4")

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
