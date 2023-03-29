# browse


import math

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from idlelib.tooltip import Hovertip

from bfsearch import core, data
from bfsearch.core import Facility
from bfsearch.data import ndict
from bfsearch.translate import tr


def getSetResultString(the_set, iv, hideItem = False, level = 50):
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
# contains an alpha/dex sortable, an iv spin box, an output and a copy to clipboard button, the facility radiobuttons, and other useful things
class SharedPageElements(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        # alphabetically organized sets
        self.sortedAlpha = ndict()
        # dex number organized sets
        self.sortedDex = ndict()

        # current set (for copy to clipboard)
        self.currentSet = None

        # facility
        self.facility = Facility.Tower

    def buildSortToggle(self, parent):
        # sort toggle button
        self.sortToggle = ttk.Button(parent, command = self.toggleSorting)
        self.alpha = True
        self.setSortToggleText()
        self.setToolTip(self.sortToggle, tr("page.generic.sortToggle.tooltip"))

    def buildIVBox(self, parent):
        # iv spin box
        self.ivLabel = ttk.Label(parent, text = tr("page.all_sets.ivs"))
        self.iv = IntVar(parent, value = 31)
        self.ivBox = ttk.Spinbox(parent, from_ = 0, to = 31, textvariable = self.iv, command = self.handleIVBox)

    def buildOutput(self, parent):
        # output
        self.output = ScrolledText(parent, width = 1, height = 1, wrap = 'word', state = 'disabled')
        # copy to clipboard button
        self.clipboardButton = ttk.Button(parent, command = self.copyToClipboard)

    def buildFacility(self, parent):
        # facility selector
        self.facilitySelect = ttk.Frame(parent, padding = (5, 0, 5, 5))
        for i in range(0, 5):
            self.facilitySelect.columnconfigure(i, weight = 1)
        self.facilitySelect.rowconfigure(0, weight = 1)

        self.facilityVar = IntVar(self.facilitySelect, value = Facility.Tower.value)
        self.towerRadio = ttk.Radiobutton(self.facilitySelect, text = tr("page.generic.facility.tower"), variable = self.facilityVar, value = Facility.Tower.value, command = self.setFacility)
        self.towerRadio.grid(column = 0, row = 0, sticky = (W, E), padx = 5)
        self.setToolTip(self.towerRadio, tr("page.generic.facility.tower.tooltip"))
        self.arcadeRadio = ttk.Radiobutton(self.facilitySelect, text = tr("page.generic.facility.arcade"), variable = self.facilityVar, value = Facility.Arcade.value, command = self.setFacility)
        self.arcadeRadio.grid(column = 1, row = 0, sticky = (W, E), padx = 5)
        self.setToolTip(self.arcadeRadio, tr("page.generic.facility.arcade.tooltip"))
        self.castleRadio = ttk.Radiobutton(self.facilitySelect, text = tr("page.generic.facility.castle"), variable = self.facilityVar, value = Facility.Castle.value, command = self.setFacility)
        self.castleRadio.grid(column = 2, row = 0, sticky = (W, E), padx = 5)
        self.setToolTip(self.castleRadio, tr("page.generic.facility.castle.tooltip"))
        self.factory50Radio = ttk.Radiobutton(self.facilitySelect, text = tr("page.generic.facility.factory_50"), variable = self.facilityVar, value = Facility.Factory_50.value, command = self.setFacility)
        self.factory50Radio.grid(column = 3, row = 0, sticky = (W, E), padx = 5)
        self.setToolTip(self.factory50Radio, tr("page.generic.facility.factory_50.tooltip"))
        self.factoryOpenRadio = ttk.Radiobutton(self.facilitySelect, text = tr("page.generic.facility.factory_open"), variable = self.facilityVar, value = Facility.Factory_Open.value, command = self.setFacility)
        self.factoryOpenRadio.grid(column = 4, row = 0, sticky = (W, E), padx = 5)
        self.setToolTip(self.factoryOpenRadio, tr("page.generic.facility.factory_open.tooltip"))

    def gridSortToggle(self, column, row):
        self.sortToggle.grid(column = column, row = row, sticky = (W, E), padx = 5)

    def gridIVBox(self, column, row):
        self.ivLabel.grid(column = column, row = row)
        self.ivBox.grid(column = column + 1, row = row, sticky = (W, E), padx = 1)

    def gridOutput(self, column, row):
        self.output.grid(column = column, row = row, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.clipboardButton.grid(column = column, row = row + 1, sticky = (W, N, E, S))

    def gridFacility(self, column, row):
        self.facilitySelect.grid(column = column, row = row, sticky = (W, N, E, S))

    # adds a simple combobox with default padx 1
    def addSimpleCombobox(self, var, command, parent, column, row, padx = 1):
        combo = ttk.Combobox(parent, textvariable = var)
        if command is not None:
            combo.bind('<<ComboboxSelected>>', command)
        combo.state(["readonly"])
        combo.grid(column = column, row = row, sticky = (W, E), padx = padx)
        return combo

    # adds a simple label to the column and row
    def addSimpleLabel(self, parent, name, column, row, tooltip = None):
        label = ttk.Label(parent, text = name)
        if tooltip is not None:
            self.setToolTip(label, tooltip)
        label.grid(column = column, row = row)
        return label

    # sets the widget's tooltip
    def setToolTip(self, widget, text, hover_delay = 1000):
        # if the widget was already given a tooltip, we adjust that one instead.
        # if you just make a brand new tooltip, there's a weird issue with comboboxes:
        # if the tooltip is open when you scroll to another entry which changes the tooltip, the old tooltip would end up sticking around.
        if hasattr(widget, 'my_tooltip'):
            widget.my_tooltip.text = text
            widget.my_tooltip.hover_delay = hover_delay
            # if the tooltip is already open, refresh it
            if widget.my_tooltip.tipwindow:
                widget.my_tooltip.hidetip()
                widget.my_tooltip.showtip()
        else:
            widget.my_tooltip = Hovertip(widget, text, hover_delay = hover_delay)

    # sets the combo box to the contents
    def fillCombobox(self, combo, contents, var):
        contents = tuple(contents)
        combo['values'] = contents
        # disable if there's only one option
        if len(contents) > 1:
            combo.state(["!disabled"])
        else:
            combo.state(["disabled"])
        # manually ensure the combobox var is valid
        if len(contents) > 0:
            var.set(contents[0])
        else:
            var.set(var._default)
        # manually generate the combobox selected event
        combo.event_generate("<<ComboboxSelected>>")

    # sets the combo box to the keys of the dict
    def fillComboboxKeys(self, combo, adict, var):
        self.fillCombobox(combo, adict.keys(), var)

    def setOutputText(self, text):
        self.output['state'] = 'normal'
        self.output.delete('1.0', 'end')
        self.output.insert('end', text)
        self.output['state'] = 'disabled'

    ### override and call super to add functionality
    def toggleSorting(self):
        self.alpha = not self.alpha
        self.setSortToggleText()

    def setSortToggleText(self):
        if self.alpha:
            self.sortToggle['text'] = tr("page.generic.sortToggle.alpha")
        else:
            self.sortToggle['text'] = tr("page.generic.sortToggle.dex")

    def getSorted(self):
        return self.getSortedAlpha() if self.alpha else self.getSortedDex()

    def getSortedAlpha(self):
        return self.sortedAlpha

    def getSortedDex(self):
        return self.sortedDex

    def setIVBox(self, minIV, maxIV):
        self.ivBox['from_'] = minIV
        self.ivBox['to'] = maxIV
        if minIV == maxIV:
            self.setToolTip(self.ivBox, tr("page.all_sets.ivBox.tooltip.fixed"))
            self.ivBox.state(["disabled"])
        else:
            self.setToolTip(self.ivBox, tr("page.generic.range", self.ivBox['from'], self.ivBox['to']))
            self.ivBox.state(["!disabled"])
        # manually ensure the spinbox var is valid
        if self.iv.get() > maxIV:
            self.iv.set(maxIV)
        if self.iv.get() < minIV:
            self.iv.set(minIV)
        # manually notify the spinbox that it changed
        self.handleIVBox()

    def setFacility(self):
        try:
            self.facility = Facility(self.facilityVar.get())
        except ValueError:
            self.facility = Facility.Tower
            self.facilityVar.set(Facility.Tower.value)
        self.handleFacility()

    def getIV(self):
        return self.iv.get()

    def getHideItem(self):
        return self.facility.hideItem()

    def getLevel(self):
        return self.facility.level()

    def validCurrentSet(self):
        return isinstance(self.currentSet, core.PokeSetBase)

    def updateOutput(self):
        if self.validCurrentSet():
            self.setOutputText(getSetResultString(self.currentSet, self.getIV(), hideItem = self.getHideItem(), level = self.getLevel()))

    def handleIVBox(self):
        self.updateSet()

    def handleFacility(self):
        self.updateSet()

    ### override and call super to add functionality
    def updateSet(self):
        self.clipboardButton['text'] = tr("page.generic.clipboardButton")

    def copyToClipboard(self):
        if self.validCurrentSet():
            self.clipboard_clear()
            self.clipboard_append(self.currentSet.getShowdownFormat(self.getIV(), hideItem = self.getHideItem(), level = self.getLevel()))
            self.clipboardButton['text'] = tr("page.generic.clipboardButton.copied")


# base page for single set browsing
class BrowseSetsPageBase(SharedPageElements):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.mainBox = ttk.Labelframe(self, text = "")

        ## set selector
        self.setSelect = ttk.Frame(self.mainBox, padding = (5, 5, 5, 0))
        for i in range(0, 5):
            self.setSelect.columnconfigure(i, weight = 1)
        self.setSelect.rowconfigure(0, weight = 1)

        # species & set combo boxes
        self.pokeLabel = self.addSimpleLabel(self.setSelect, tr("page.generic.pokemon"), 0, 0)
        self.poke = StringVar(self.setSelect)
        self.pokeCombo = self.addSimpleCombobox(self.poke, self.handlePokeCombo, self.setSelect, 1, 0)
        self.set = IntVar(self.setSelect)
        self.setCombo = self.addSimpleCombobox(self.set, self.handleSetCombo, self.setSelect, 2, 0)

        # iv spin box
        self.buildIVBox(self.setSelect)
        self.gridIVBox(3, 0)

        # sort toggle
        self.buildSortToggle(self.mainBox)

        # output & clipboard options
        self.buildOutput(self.mainBox)

        # facility selector
        self.buildFacility(self.mainBox)

        # set up initial state
        self.updateSet()

    def gridSetSelect(self, column, row):
        self.setSelect.grid(column = column, row = row, sticky = (W, N, E, S))

    def toggleSorting(self):
        super().toggleSorting()
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)

    # when the species combo box updates, tells the set combo box to update
    def handlePokeCombo(self, event = None):
        setsData = self.getSorted()[self.poke.get()]
        self.fillComboboxKeys(self.setCombo, setsData, self.set)
        count = len(self.setCombo['values'])
        if count == 1:
            self.setToolTip(self.setCombo, tr("page.all_sets.setCombo.tooltip.singular", count))
        else:
            self.setToolTip(self.setCombo, tr("page.all_sets.setCombo.tooltip.plural", count))

    def handleSetCombo(self, event = None):
        self.updateSet()

    def updateSet(self):
        super().updateSet()
        self.currentSet = self.getSorted()[self.poke.get()][self.set.get()]
        if self.validCurrentSet():
            self.updateOutput()
            self.clipboardButton.state(["!disabled"])
            self.setToolTip(self.pokeCombo, str(self.currentSet.species))
        else:
            self.clearResults()

    def clearResults(self):
        self.setOutputText(tr("page.all_sets.empty_results"))
        self.clipboardButton.state(["disabled"])
        self.setToolTip(self.pokeCombo, "")
        self.setToolTip(self.setCombo, "")


# browse all sets
class BrowseAllSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, setProvider):
        super().__init__(parent)

        # build
        self.setProvider = setProvider
        self.sortedAlpha = data.setsAlphaSorted(self.setProvider.sets)
        self.sortedDex = data.setsDexSorted(self.setProvider.sets)
        self.setIVBox(0, 31)

        # place the main box
        self.gridFacility(0, 0)
        self.gridSortToggle(0, 1)
        self.gridSetSelect(0, 2)
        self.gridOutput(0, 3)
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(3, weight = 1)

        # place this tab
        infoLabel = ttk.Label(self, text = tr("page.all_sets.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.setToolTip(self.pokeLabel, tr("page.all_sets.pokemon.tooltip"))
        self.setToolTip(self.ivLabel, tr("page.all_sets.ivs.tooltip"))

        # set up initial state
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)


# browse sets by trainer
class BrowseTrainerSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, facilities):
        super().__init__(parent)

        # build
        self.facilities = facilities

        # place the main box
        ## trainer selector
        trainerSelect = ttk.Frame(self.mainBox, padding = (5, 0, 5, 5))
        for i in range(0, 5):
            trainerSelect.columnconfigure(i, weight = 1)
        trainerSelect.rowconfigure(0, weight = 1)

        # battle number combo box
        self.battlenumLabel = self.addSimpleLabel(trainerSelect, tr("page.generic.battle_number"), 0, 0, tooltip = tr("page.all_sets_by_trainer.battle_number.tooltip"))
        self.battlenum = StringVar(trainerSelect)
        self.battlenumCombo = self.addSimpleCombobox(self.battlenum, self.handleBattlenumCombo, trainerSelect, 1, 0)

        # trainer class & name combo boxes
        self.trainerLabel = self.addSimpleLabel(trainerSelect, tr("page.generic.trainer"), 2, 0, tooltip = tr("page.all_sets_by_trainer.trainer.tooltip"))
        self.tclass = StringVar(trainerSelect)
        self.tclassCombo = self.addSimpleCombobox(self.tclass, self.handleTClassCombo, trainerSelect, 3, 0)
        self.tname = StringVar(trainerSelect)
        self.tnameCombo = self.addSimpleCombobox(self.tname, self.handleTNameCombo, trainerSelect, 4, 0)

        self.gridFacility(0, 0)
        trainerSelect.grid(column = 0, row = 1, sticky = (W, N, E, S))
        self.gridSortToggle(0, 2)
        self.gridSetSelect(0, 3)
        self.gridOutput(0, 4)
        self.darachLabel = ttk.Label(self.mainBox, text = tr("page.all_sets_by_trainer.darach"))
        self.thortonLabel = ttk.Label(self.mainBox, text = tr("page.all_sets_by_trainer.thorton"))
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(4, weight = 1)

        # place this tab
        infoLabel = ttk.Label(self, text = tr("page.all_sets_by_trainer.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.setToolTip(self.pokeLabel, tr("page.all_sets_by_trainer.pokemon.tooltip"))
        self.setToolTip(self.ivLabel, tr("page.all_sets_by_trainer.ivs.tooltip"))

        # set up initial state
        self.prepFacility()
        self.fillComboboxKeys(self.battlenumCombo, self.bTSP(), self.battlenum)

    def bTSP(self):
        return self.battlenumToSetProviders

    def prepFacility(self):
        self.battlenumToSetProviders = data.battlenumToGroupedSetProviders(self.facilities[self.facility])

    # when the facility selection changes, tells the trainer class combo box to update
    def handleFacility(self):
        self.prepFacility()
        self.handleBattlenumCombo()

    # when the battle number combo box updates, tells the trainer class combo box to update
    def handleBattlenumCombo(self, event = None):
        tclassData = self.bTSP()[self.battlenum.get()]
        self.fillComboboxKeys(self.tclassCombo, tclassData, self.tclass)

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self, event = None):
        tnameData = self.bTSP()[self.battlenum.get()][self.tclass.get()]
        self.fillComboboxKeys(self.tnameCombo, tnameData, self.tname)
        # darach works differently from every other trainer.
        if "Castle Valet" in self.tclass.get():
            self.darachLabel.grid(column = 0, row = 6, sticky = (W, N, E, S), padx = 5, pady = 5)
        else:
            self.darachLabel.grid_forget()
        # missing thorton data...
        if "Factory Head" in self.tclass.get():
            self.thortonLabel.grid(column = 0, row = 6, sticky = (W, N, E, S), padx = 5, pady = 5)
        else:
            self.thortonLabel.grid_forget()

    def handleTNameCombo(self, event = None):
        self.updateTrainer()

    def updateTrainer(self):
        currentProvider = self.bTSP()[self.battlenum.get()][self.tclass.get()][self.tname.get()]
        if isinstance(currentProvider, core.SetProvider):
            self.sortedAlpha = data.setsAlphaSorted(currentProvider.sets)
            self.sortedDex = data.setsDexSorted(currentProvider.sets)
            # when the trainer selection updates, tells the species combo box to update
            self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)
            self.setIVBox(currentProvider.minIV, currentProvider.maxIV)
            self.setToolTip(self.battlenumCombo, self.battlenum.get())
            self.setToolTip(self.tclassCombo, self.tclass.get())
            self.setToolTip(self.tnameCombo, self.tname.get())
        else:
            self.clearTrainerResults()

    def clearTrainerResults(self):
        self.sortedAlpha = ndict()
        self.sortedDex = ndict()
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)
        self.setIVBox(0, 0)
        self.setToolTip(self.battlenumCombo, "")
        self.setToolTip(self.tclassCombo, "")
        self.setToolTip(self.tnameCombo, "")
