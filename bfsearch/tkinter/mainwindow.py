# mainwindow


import sys, logging

from tkinter import *
from tkinter import ttk
from idlelib.tooltip import Hovertip

from bfsearch import data, translate, settings
from bfsearch.translate import tr
from bfsearch.tkinter import browse, search, browsehall



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
        self.bficon = PhotoImage(file = "gui/icon.png")
        self.wm_iconphoto(True, self.bficon)
        self.minsize(750, 607)
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
        self.tabs.add(self.createStartPage(), text = tr("page.welcome.name"), image = self.bficon, compound = 'left')

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

        self.browseTrainerSetsPage = browse.BrowseTrainerSetsPage(self.tabs, data.battlenumToGroupedSetProviders(self.data.trainers))
        self.trainerImage = PhotoImage(file = "gui/trainers.png")
        self.tabs.add(self.browseTrainerSetsPage, text = tr("page.all_sets_by_trainer.name"), image = self.trainerImage, compound = 'left')
        #tr("page.all_sets_by_trainer.tooltip")

        self.searchPage = search.SearchPage(self, self.data)
        self.searchImage = PhotoImage(file = "gui/search.png")
        self.tabs.add(self.searchPage, text = tr("page.search.name"), image = self.searchImage, compound = 'left')
        #tr("page.search.tooltip")

        self.browseHallSetsPage = browsehall.BrowseAllHallSetsPage(self, data.genericSetProvider(self.data.hall_sets))
        self.hallImage = PhotoImage(file = "gui/hallpokemon.png")
        self.tabs.add(self.browseHallSetsPage, text = tr("page.hall_sets.name"), image = self.hallImage, compound = 'left')
        #tr("page.hall_sets.tooltip")

        self.calcHallSetsPage = browsehall.CalcHallSetsPage(self, data.typeToRankToHallSets(self.data.hall_sets), data.hallSetGroupToHallSets(self.data.hall_sets))
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
        aboutdialog = ButtonDialog(self._root(), tr("toolbar.button.about.name"), tr("toolbar.button.about.about"), "gui/about.png", [tr("toolbar.button.ok"), tr("toolbar.button.about.linkButton")])
        pressed = aboutdialog.show()
        if pressed == 1:
            self.clipboard_clear()
            self.clipboard_append("https://calc.pokemonshowdown.com/index.html?gen=4")

    def showLang(self):
        prettyDict = translate.prettyLangsDict()
        note = tr("toolbar.button.language.note")
        if len(prettyDict) <= 1:
            note += "\n" + tr("toolbar.button.language.note.single")
        langdialog = ComboboxDialog(self._root(), tr("toolbar.button.language.name"), note, "gui/language.png", [tr("toolbar.button.ok"), tr("toolbar.button.cancel")], contents = prettyDict.keys(), default = translate.currentLangIndex())
        pressed, combo = langdialog.show()
        if pressed == 0 and combo in prettyDict.keys():
            lang = prettyDict[combo]
            if lang != translate.currentLang:
                translate.currentLang = lang
                logging.info("Changed language!")
                settings.settings[translate.settingsKey] = lang
                settings.save()
                CURRENT_CODE[0] = RECREATE_CODE
                self._root().destroy()


# a dialog with text, and image, and buttons. inspired by/copied from tkinter.simpledialog.SimpleDialog.
# returns the index of the button pressed, or -1 if the window was closed with the X button or by pressing escape.
class ButtonDialog(object):
    # imagepath is a path to an image. buttons is a list of names of buttons.
    def __init__(self, parent, title, text, imagepath, buttons, **kwargs):
        self.top = Toplevel(parent)
        self.top.title(title)

        self.pressed = -1

        self.buildDialog(text = text, imagepath = imagepath, buttons = buttons, **kwargs)

        # 'dlings' if you click on the main window while this dialog is still open
        self.top.bind("<Button-1>", self.check_outside)

        self.top.bind('<Escape>', self.cancel_window)
        self.top.protocol('WM_DELETE_WINDOW', self.cancel_window)
        self._set_transient(parent)
        self.top.resizable(False, False)

    def buildDialog(self, **kwargs):
        self.mainframe = ttk.Frame(self.top)
        self.mainframe.grid(column = 0, row = 0, sticky = (W, N, E, S), ipadx = 10, ipady = 5)
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.columnconfigure(1, weight = 1)

        self.image = PhotoImage(file = kwargs['imagepath'])
        self.imagelabel = ttk.Label(self.mainframe, image = self.image, padding = (10, 5, 0, 5))
        self.imagelabel.grid(column = 0, row = 0, sticky = (W, N, E, S))

        styler = ttk.Style()
        self.mainlabel = ttk.Label(self.mainframe, text = kwargs['text'], wraplength = 450, padding = (0, 5, 10, 5))
        self.mainlabel.grid(column = 1, row = 0, sticky = (W, N, E, S))

        self.buttonframe = ttk.Frame(self.top, padding = (10, 0, 15, 10))
        self.buttonframe.columnconfigure(0, weight = 1)
        self.buttonframe.grid(column = 0, row = 1, sticky = (W, N, E, S))
        for index, name in enumerate(kwargs['buttons']):
            button = Button(self.buttonframe, text = name, command = (lambda self = self, index = index: self.finish(index)))
            button.grid(column = index, row = 0, sticky = (E, S), padx = 5, ipadx = 20)
            if index == 0:
                button.focus_set()

    # copy-pasted window centerer thing
    def _set_transient(self, parent, relx = 0.5, rely = 0.3):
        widget = self.top
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(parent)
        widget.update_idletasks() # Actualize geometry information
        if parent.winfo_ismapped():
            m_width = parent.winfo_width()
            m_height = parent.winfo_height()
            m_x = parent.winfo_rootx()
            m_y = parent.winfo_rooty()
        else:
            m_width = parent.winfo_screenwidth()
            m_height = parent.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > parent.winfo_screenwidth():
            x = parent.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > parent.winfo_screenheight():
            y = parent.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location

    def check_outside(self, event):
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        if event.x < 0 or event.x > width or event.y < 0 or event.y > height:
            self.top.bell()

    def cancel_window(self, event = None):
        self.finish(-1)

    def finish(self, pressed):
        self.pressed = pressed
        self.top.quit()

    def show(self):
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.mainloop()
        self.top.destroy()
        return self.output()

    def output(self):
        return self.pressed

# button dialog box that also has a combobox. 
# along with the index of the button pressed, returns the selection in the combobox.
class ComboboxDialog(ButtonDialog):
    # contents is a list of values to put in the combobox. default is the index the combobox should start at.
    def __init__(self, parent, title, text, image, buttons, contents, default = 0):
        ButtonDialog.__init__(self, parent, title, text, image, buttons, contents = contents, default = default)

    def buildDialog(self, **kwargs):
        super().buildDialog(**kwargs)

        self.combo = StringVar(self.mainframe)
        values = tuple(kwargs['contents'])
        self.combobox = ttk.Combobox(self.mainframe, textvariable = self.combo, values = values)
        self.combobox.state(["readonly"])
        self.combobox.grid(column = 0, row = 1, columnspan = 2, sticky = (W, N, E, S), padx = 30, pady = 5)
        default = kwargs['default']
        if default in range(len(values)):
            self.combobox.current(default)
        self.combobox.focus_set()

    def output(self):
        return self.pressed, self.combo.get()
