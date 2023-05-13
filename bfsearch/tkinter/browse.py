# browse


from tkinter import *
from tkinter import ttk

from bfsearch import data
from bfsearch.data import ndict
from bfsearch.tkinter import common
from bfsearch.translate import tr


# base page for single set browsing
class BrowseSetsPageBase(common.SharedPageElements):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.mainBox = ttk.Labelframe(self, text = "")

        ## set selector
        self.setSelect = ttk.Frame(self.mainBox, padding = (5, 5, 5, 0))
        for i in range(0, 11):
            self.setSelect.columnconfigure(i, weight = 1)
        self.setSelect.rowconfigure(0, weight = 1)

        # group combo
        self.buildGroupCombo(self.setSelect)
        self.gridGroupCombo(0, 0)

        # species & set combo boxes
        self.pokeLabel = self.addSimpleLabel(self.setSelect, tr("page.generic.pokemon"), 2, 0)
        self.poke = StringVar(self.setSelect)
        self.pokeCombo = self.addSimpleCombobox(self.poke, self.handlePokeCombo, self.setSelect, 3, 0)
        self.setLabel = self.addSimpleLabel(self.setSelect, tr("page.generic.set_number"), 4, 0, tooltip = tr("page.generic.set_number.tooltip"))
        self.set = IntVar(self.setSelect)
        # possible set numbers for the current pokemon
        self.possibleSets = []
        valuesGetter = lambda: self.possibleSets
        self.setRadio1 = self.addScrollableRadioButton(self.setSelect, 1, self.set, 1, valuesGetter, self.handleSetRadio, 5, 0)
        self.setRadio2 = self.addScrollableRadioButton(self.setSelect, 2, self.set, 2, valuesGetter, self.handleSetRadio, 6, 0)
        self.setRadio3 = self.addScrollableRadioButton(self.setSelect, 3, self.set, 3, valuesGetter, self.handleSetRadio, 7, 0)
        self.setRadio4 = self.addScrollableRadioButton(self.setSelect, 4, self.set, 4, valuesGetter, self.handleSetRadio, 8, 0)
        # scroll when hovering on the label as well
        self.setLabel.bind('<MouseWheel>', lambda event: self.scrollRadio(event, self.set, valuesGetter, self.handleSetRadio))

        # iv spin box
        self.buildIVBox(self.setSelect)
        self.gridIVBox(9, 0)

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

    def filterByGroup(self, sortedData):
        if self.group.get() == data.emptyKey:
            return sortedData
        else:
            return data.filterSetsByGroup(sortedData, self.group.get())

    # when the group combo box updates, tells the species combo box to update
    def handleGroupCombo(self, event = None):
        if self.group.get() == data.emptyKey:
            self.setToolTip(self.groupCombo, tr("page.generic.tooltip.empty_key"))
        else:
            self.setToolTip(self.groupCombo, tr(f"page.all_sets.group.tooltip.{self.group.get().lower()}"))
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)

    # when the species combo box updates, tells the set radio buttons to update
    def handlePokeCombo(self, event = None):
        self.possibleSets = list(self.getSorted()[self.poke.get()].keys())
        def setRadioState(radio, num):
            if num in self.possibleSets:
                radio.state(['!disabled'])
                self.setToolTip(radio, self.poke.get() + " " + str(num))
            else:
                radio.state(['disabled'])
                self.setToolTip(radio, tr("page.generic.set_number.not_available"))
        setRadioState(self.setRadio1, 1)
        setRadioState(self.setRadio2, 2)
        setRadioState(self.setRadio3, 3)
        setRadioState(self.setRadio4, 4)
        if self.possibleSets:
            self.set.set(self.possibleSets[0])
        else:
            self.set.set(self.set._default)
        self.handleSetRadio()

    def handleSetRadio(self, event = None):
        self.updateSet()

    def updateSet(self):
        super().updateSet()
        self.currentSet = self.getSorted()[self.poke.get()][self.set.get()]
        if self.currentSet:
            self.updateOutput()
            self.clipboardButton.state(["!disabled"])
            self.setToolTip(self.pokeCombo, str(self.currentSet.species))
        else:
            self.clearResults()

    def clearResults(self):
        self.setOutputText(tr("page.all_sets.empty_results"))
        self.clipboardButton.state(["disabled"])
        self.setToolTip(self.pokeCombo, "")


# browse all sets
class BrowseAllSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, setProvider):
        super().__init__(parent)

        # build
        self.setProvider = setProvider
        self.sortedAlpha = data.setsAlphaSorted(self.setProvider.sets)
        self.sortedDex = data.setsDexSorted(self.setProvider.sets)

        # place the main box
        self.gridFacility(0, 0)
        self.gridSortToggle(0, 1)
        self.gridSetSelect(0, 2)
        self.gridOutput(0, 3)
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(3, weight = 1)

        # place this tab
        infoLabel = self.buildSimpleLabel(self, tr("page.all_sets.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

        # set up initial state
        self.fillGroupCombo(sorted({setgroup.mainGroup() for setgroup in self.setProvider.setgroups}))
        self.prepFacility()

    def prepFacility(self):
        self.setIVBox(self.facility.ivValues())

    # when the facility selection changes, update the possible ivs
    def handleFacility(self):
        self.prepFacility()


# browse sets by trainer
class BrowseTrainerSetsPage(BrowseSetsPageBase):
    def __init__(self, parent, facilities):
        super().__init__(parent)

        # build
        self.facilities = facilities

        # remove group combo
        self.groupLabel.grid_forget()
        self.groupCombo.grid_forget()
        self.setSelect.columnconfigure(0, weight = 0)
        self.setSelect.columnconfigure(1, weight = 0)

        # place the main box
        ## trainer selector
        trainerSelect = ttk.Frame(self.mainBox, padding = (5, 0, 5, 5))
        for i in range(0, 5):
            trainerSelect.columnconfigure(i, weight = 1)
        trainerSelect.rowconfigure(0, weight = 1)

        # battle number combo box
        self.battlenumLabel = self.addSimpleLabel(trainerSelect, tr("page.generic.battle_number"), 0, 0)
        self.battlenum = StringVar(trainerSelect)
        self.battlenumCombo = self.addSimpleCombobox(self.battlenum, self.handleBattlenumCombo, trainerSelect, 1, 0)
        self.battlenumCombo['width'] = 11

        # trainer class & name combo boxes
        self.trainerLabel = self.addSimpleLabel(trainerSelect, tr("page.generic.trainer"), 2, 0)
        self.tclass = StringVar(trainerSelect)
        self.tclassCombo = self.addSimpleCombobox(self.tclass, self.handleTClassCombo, trainerSelect, 3, 0)
        self.tname = StringVar(trainerSelect)
        self.tnameCombo = self.addSimpleCombobox(self.tname, self.handleTNameCombo, trainerSelect, 4, 0)

        self.gridFacility(0, 0)
        trainerSelect.grid(column = 0, row = 1, sticky = (W, N, E, S))
        self.gridSortToggle(0, 2)
        self.gridSetSelect(0, 3)
        self.gridOutput(0, 4)
        self.thortonLabel = self.buildSimpleLabel(self.mainBox, tr("page.all_sets_by_trainer.thorton"))
        self.mainBox.columnconfigure(0, weight = 1)
        self.mainBox.rowconfigure(4, weight = 1)

        # place this tab
        infoLabel = self.buildSimpleLabel(self, tr("page.all_sets_by_trainer.info"))
        infoLabel.grid(column = 0, row = 0, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.mainBox.grid(column = 0, row = 1, sticky = (N, S, E, W), padx = 5, pady = 5)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

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
        # maintain selections if possible
        def maintainCombo(combo, prevValue, var):
            try:
                var.set(combo['values'][combo['values'].index(prevValue)])
                combo.event_generate("<<ComboboxSelected>>")
            except ValueError:
                pass
        prevTClass = self.tclass.get()
        prevTName = self.tname.get()
        prevPoke = self.poke.get()
        prevSet = self.set.get()
        self.handleBattlenumCombo()
        maintainCombo(self.tclassCombo, prevTClass, self.tclass)
        maintainCombo(self.tnameCombo, prevTName, self.tname)
        maintainCombo(self.pokeCombo, prevPoke, self.poke)
        if prevSet in self.possibleSets:
            self.set.set(prevSet)
            self.handleSetRadio()

    # when the battle number combo box updates, tells the trainer class combo box to update
    def handleBattlenumCombo(self, event = None):
        tclassData = self.bTSP()[self.battlenum.get()]
        self.fillComboboxKeys(self.tclassCombo, tclassData, self.tclass)

    # when the trainer class combo box updates, tells the trainer name combo box to update
    def handleTClassCombo(self, event = None):
        tnameData = self.bTSP()[self.battlenum.get()][self.tclass.get()]
        self.fillComboboxKeys(self.tnameCombo, tnameData, self.tname)
        # missing thorton data...
        if "Factory Head" in self.tclass.get():
            self.thortonLabel.grid(column = 0, row = 6, sticky = (W, N, E, S), padx = 5, pady = 5)
        else:
            self.thortonLabel.grid_forget()

    def handleTNameCombo(self, event = None):
        self.updateTrainer()

    def updateTrainer(self):
        currentProvider = self.bTSP()[self.battlenum.get()][self.tclass.get()][self.tname.get()]
        if currentProvider:
            self.sortedAlpha = data.setsAlphaSorted(currentProvider.sets)
            self.sortedDex = data.setsDexSorted(currentProvider.sets)
            # when the trainer selection updates, tells the species combo box to update
            self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)
            self.setIVBox([currentProvider.iv])
            if self.battlenum.get() == data.emptyKey:
                self.setToolTip(self.battlenumCombo, tr("page.generic.tooltip.empty_key"))
            else:
                self.setToolTip(self.battlenumCombo, self.battlenum.get())
            self.setToolTip(self.tclassCombo, self.tclass.get())
            self.setToolTip(self.tnameCombo, self.tname.get())
        else:
            self.clearTrainerResults()

    def clearTrainerResults(self):
        self.sortedAlpha = ndict()
        self.sortedDex = ndict()
        self.fillComboboxKeys(self.pokeCombo, self.getSorted(), self.poke)
        self.setIVBox([0])
        self.setToolTip(self.battlenumCombo, "")
        self.setToolTip(self.tclassCombo, "")
        self.setToolTip(self.tnameCombo, "")
