# common


import math

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from idlelib.tooltip import Hovertip

from bfsearch import data
from bfsearch.core import Facility
from bfsearch.data import ndict
from bfsearch.translate import tr


def getSetResultString(the_set, iv, hideItem = False, level = 50):
    string = the_set.getShowdownFormat(iv, hideItem = hideItem, level = level)
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
    #string += "\nSet Group: " + the_set.setgroup.name + "\n"
    #string += "\nTypes: " + str(the_set.species.types) + "\n"
    return string


# base class for functional pages
class SharedPageElements(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.clearSorted()

        # current set (for copy to clipboard)
        self.currentSet = None

        # facility
        self.facility = Facility.Tower

    def clearSorted(self):
        # alphabetically organized sets
        self.sortedAlpha = ndict()
        # dex number organized sets
        self.sortedDex = ndict()

    def buildSortToggle(self, parent):
        # sort toggle button
        self.sortToggle = ttk.Button(parent, command = self.toggleSorting)
        self.alpha = True
        self.setSortToggleText()
        self.setToolTip(self.sortToggle, tr("page.generic.sortToggle.tooltip"))

    def buildGroupCombo(self, parent):
        # group combo box
        self.groupLabel = self.buildSimpleLabel(parent, tr("page.all_sets.group"))
        self.group = StringVar(parent, value = data.emptyKey)
        self.groupCombo = self.buildSimpleCombobox(self.group, self.handleGroupCombo, parent)
        self.groupCombo['width'] = 7

    def buildPokeCombo(self, parent):
        # poke combo box
        self.pokeLabel = self.buildSimpleLabel(parent, tr("page.generic.pokemon"))
        self.poke = StringVar(parent)
        self.pokeCombo = self.buildSimpleCombobox(self.poke, self.handlePokeCombo, parent)

    def buildIVBox(self, parent):
        # iv spin box
        self.ivLabel = self.buildSimpleLabel(parent, tr("page.all_sets.ivs"))
        self.iv = IntVar(parent, value = 31)
        self.ivBox = ttk.Spinbox(parent, from_ = 0, to = 31, textvariable = self.iv, command = self.handleIVBox, width = 5)

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

    def gridGroupCombo(self, column, row):
        self.groupLabel.grid(column = column, row = row)
        self.groupCombo.grid(column = column + 1, row = row, sticky = (W, E), padx = 1)

    def gridPokeCombo(self, column, row):
        self.pokeLabel.grid(column = column, row = row)
        self.pokeCombo.grid(column = column + 1, row = row, sticky = (W, E), padx = 1)

    def gridIVBox(self, column, row):
        self.ivLabel.grid(column = column, row = row)
        self.ivBox.grid(column = column + 1, row = row, sticky = (W, E), padx = 1)

    def gridOutput(self, column, row):
        self.output.grid(column = column, row = row, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.clipboardButton.grid(column = column, row = row + 1, sticky = (W, N, E, S))

    def gridFacility(self, column, row):
        self.facilitySelect.grid(column = column, row = row, sticky = (W, N, E, S))

    # makes a combobox
    def buildSimpleCombobox(self, var, command, parent):
        combo = ttk.Combobox(parent, textvariable = var)
        if command is not None:
            combo.bind('<<ComboboxSelected>>', command)
        combo.state(["readonly"])
        return combo

    # adds a combobox with default padx 1
    def addSimpleCombobox(self, var, command, parent, column, row, padx = 1):
        combo = self.buildSimpleCombobox(var, command, parent)
        combo.grid(column = column, row = row, sticky = (W, E), padx = padx)
        return combo

    # makes a label with an appropriate wraplength
    def buildSimpleLabel(self, parent, name, tooltip = None):
        label = ttk.Label(parent, text = name, wraplength = 730)
        if tooltip is not None:
            self.setToolTip(label, tooltip)
        return label

    # adds a label to the column and row
    def addSimpleLabel(self, parent, name, column, row, tooltip = None):
        label = self.buildSimpleLabel(parent, name, tooltip)
        label.grid(column = column, row = row)
        return label

    # adds a radio button that can be scrolled. valuesGetter is a function that returns the current possible values the radio buttons can have.
    def addScrollableRadioButton(self, parent, text, var, value, valuesGetter, command, column, row):
        radio = ttk.Radiobutton(parent, text = text, variable = var, value = value, command = command)
        radio.bind('<MouseWheel>', lambda event: self.scrollRadio(event, var, valuesGetter, command))
        radio.grid(column = column, row = row, sticky = (W, E))
        return radio

    def scrollRadio(self, event, var, valuesGetter, command):
        if valuesGetter():
            try:
                currentIndex = valuesGetter().index(var.get())
                if event.delta > 0:
                    if currentIndex > 0:
                        var.set(valuesGetter()[currentIndex - 1])
                        command()
                elif event.delta < 0:
                    if currentIndex < len(valuesGetter()) - 1:
                        var.set(valuesGetter()[currentIndex + 1])
                        command()
            except ValueError:
                var.set(valuesGetter()[0])
                command()

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

    # sets the combo box to the contents, plus an empty entry at the start
    def fillComboboxPlusEmpty(self, combo, contents, var):
        contents = (data.emptyKey, *contents)
        self.fillCombobox(combo, contents, var)

    def setOutputText(self, text):
        self.output['state'] = 'normal'
        self.output.delete('1.0', 'end')
        self.output.insert('end', text)
        self.output['state'] = 'disabled'

    def toggleSorting(self):
        self.alpha = not self.alpha
        self.setSortToggleText()
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)

    def setSortToggleText(self):
        if self.alpha:
            self.sortToggle['text'] = tr("page.generic.sortToggle.alpha")
        else:
            self.sortToggle['text'] = tr("page.generic.sortToggle.dex")

    def getSorted(self):
        return self.filterByGroup(self.sortedAlpha if self.alpha else self.sortedDex)

    ### override if using group combo
    def filterByGroup(self, sortedData):
        return sortedData

    # if there's more than one group, adds an empty entry at the start.
    def fillGroupCombo(self, contents):
        if len(contents) > 1:
            filler = self.fillComboboxPlusEmpty
        else:
            filler = self.fillCombobox
        filler(self.groupCombo, contents, self.group)

    def setIVBox(self, values):
        oldValues = self.ivBox['values']
        self.ivBox['values'] = values
        if len(values) > 1:
            # tooltip
            self.setToolTip(self.ivBox, ", ".join(self.ivBox['values']))
            self.ivBox.state(["!disabled"])
            # spinbox var
            index = -1
            if oldValues and len(oldValues) == len(values):
                try:
                    # tkinter turns the values into strings.
                    index = oldValues.index(str(self.iv.get()))
                except ValueError:
                    pass
            self.iv.set(values[index])
        else:
            # tooltip
            self.setToolTip(self.ivBox, tr("page.all_sets.ivBox.tooltip.fixed"))
            self.ivBox.state(["disabled"])
            # spinbox var
            if len(values) == 1:
                self.iv.set(values[0])
            else:
                self.iv.set(31)
        # manually notify the spinbox that it changed
        self.handleIVBox()

    def setFacility(self):
        try:
            self.facility = Facility(self.facilityVar.get())
        except ValueError:
            self.facility = Facility.Tower
            self.facilityVar.set(Facility.Tower.value)
        self.handleFacility()

    ### override if using facility
    def prepFacility(self):
        pass

    ### override if using facility
    def handleFacility(self):
        pass

    def getIV(self):
        return self.iv.get()

    def getHideItem(self):
        return self.facility.hideItem()

    def getLevel(self):
        return self.facility.level()

    def updateOutput(self):
        if self.currentSet:
            self.setOutputText(getSetResultString(self.currentSet, self.getIV(), hideItem = self.getHideItem(), level = self.getLevel()))

    ### override if using group combo
    def handleGroupCombo(self, event = None):
        pass

    def handleIVBox(self):
        self.updateSet()

    ### override and call super to add functionality
    def updateSet(self):
        self.clipboardButton['text'] = tr("page.generic.clipboardButton")

    def copyToClipboard(self):
        if self.currentSet:
            self.clipboard_clear()
            self.clipboard_append(self.currentSet.getShowdownFormat(self.getIV(), hideItem = self.getHideItem(), level = self.getLevel()))
            self.clipboardButton['text'] = tr("page.generic.clipboardButton.copied")
