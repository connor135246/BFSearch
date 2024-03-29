# helpdialogs


from tkinter import *
from tkinter import ttk

from bfsearch import core
from bfsearch.translate import tr
from bfsearch.tkinter import dialogs

### help dialogs todo
# arcade board: possibilities at each streak, possible random items
# sets that have return & frustration? how does friendship work?
# all about trainer ai
# allow main window to be used while help dialogs are open


# general dialogs

def mainHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.basics"), basicHelp))
    helpoptions.append((tr("help.tower"), towerHelp))
    helpoptions.append((tr("help.arcade"), arcadeHelp))
    helpoptions.append((tr("help.castle"), castleHelp))
    helpoptions.append((tr("help.factory"), factoryHelp))
    helpoptions.append((tr("help.hall"), hallHelp))
    HelpDialog(parent, tr("toolbar.button.help.name"), tr("help"), helpoptions).show()
    parent.grab_set()

def towerHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), nonhallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), nonhallGroups))
    helpoptions.append((tr("help.normal.trainer_pokemon"), normalTrainerPokemon))
    helpoptions.append((tr("help.normal.trainer_classes"), normalTrainerClasses))
    HelpDialog(parent, tr("help.tower"), tr("help_order"), helpoptions).show()
    parent.grab_set()

def arcadeHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), nonhallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), nonhallGroups))
    helpoptions.append((tr("help.normal.trainer_pokemon"), normalTrainerPokemon))
    helpoptions.append((tr("help.normal.trainer_classes"), normalTrainerClasses))
    helpoptions.append((tr("help.mechanics.arcade.board"), mechanicsArcadeBoard))
    HelpDialog(parent, tr("help.arcade"), tr("help_order"), helpoptions).show()
    parent.grab_set()

def castleHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), nonhallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), nonhallGroups))
    helpoptions.append((tr("help.normal.trainer_pokemon"), normalTrainerPokemon))
    helpoptions.append((tr("help.normal.trainer_classes"), normalTrainerClasses))
    helpoptions.append((tr("help.mechanics.castle.earning_points"), mechanicsCastleEarn))
    helpoptions.append((tr("help.mechanics.castle.spending_points"), mechanicsCastleSpend))
    helpoptions.append((tr("help.mechanics.castle.spending_points.items"), mechanicsCastleSpendItems))
    HelpDialog(parent, tr("help.castle"), tr("help_order"), helpoptions).show()
    parent.grab_set()

def factoryHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), nonhallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), nonhallGroups))
    helpoptions.append((tr("help.factory.trainer_pokemon_50"), factoryTrainerPokemon50))
    helpoptions.append((tr("help.factory.trainer_pokemon_open"), factoryTrainerPokemonOpen))
    helpoptions.append((tr("help.mechanics.factory.starting_rentals"), mechanicsFactoryRentals))
    helpoptions.append((tr("help.mechanics.factory.clauses"), mechanicsFactoryClauses))
    HelpDialog(parent, tr("help.factory"), tr("help_order"), helpoptions).show()
    parent.grab_set()

def hallHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), hallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), hallGroups))
    helpoptions.append((tr("help.hall.rank_pokemon"), hallRankPokemon))
    helpoptions.append((tr("help.hall.rank_ivs"), hallRankIVs))
    helpoptions.append((tr("help.hall.level"), hallLevel))
    HelpDialog(parent, tr("help.hall"), tr("help_order"), helpoptions).show()
    parent.grab_set()

class HelpDialog(dialogs.InfoDialog):
    # helpoptions is a list of tuples (button name, method to call).
    def __init__(self, parent, title, text, helpoptions):
        dialogs.InfoDialog.__init__(self, parent, title, [tr("toolbar.button.cancel")], text, "gui/help.png", helpoptions = helpoptions)

    def buildDialog(self, **kwargs):
        super().buildDialog(**kwargs)

        self.tbuttonframe = ttk.Frame(self.mainframe, padding = (15, 0, 15, 0))
        self.tbuttonframe.columnconfigure(0, weight = 1)
        self.tbuttonframe.grid(column = 0, row = 1, columnspan = 2, sticky = (W, N, E, S), padx = 30, pady = 5)
        for index, helpoption in enumerate(kwargs['helpoptions']):
            tbutton = ttk.Button(self.tbuttonframe, text = helpoption[0], command = (lambda method = helpoption[1]: method(self.top)))
            tbutton.grid(column = 0, row = index, sticky = (W, N, E, S), padx = 5, pady = 5, ipadx = 20)
            if index == 0:
                tbutton.focus_set()


# topic dialogs

def basicHelp(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.basics.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.basics"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def nonhallPokemon(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.nonhall.pokemon.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.nonhall.pokemon"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def nonhallGroups(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.nonhall.groups.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        groups = ['a', 'b', 'c', 'd']
        values = [tr(f"help.nonhall.groups.{group}.name") for group in groups]

        headings = [tr("help.nonhall.groups.tree.desc"), tr("help.nonhall.groups.tree.examples")]
        colsvalues = [[tr(f"help.nonhall.groups.{group}.desc"), tr(f"help.nonhall.groups.{group}.examples")] for group in groups]
        groupView = multiColTree(self.mainframe, width, tr("help.nonhall.groups.tree.name"), headings, values, colsvalues)
        groupView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.nonhall.groups.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        headings = [tr("help.nonhall.groups.tree.sets"), tr("help.nonhall.groups.tree.subs")]
        colsvalues = [[tr(f"help.nonhall.groups.{group}.sets"), tr(f"help.nonhall.groups.{group}.subs")] for group in groups]
        groupViewSets = multiColTree(self.mainframe, width, tr("help.nonhall.groups.tree.name"), headings, values, colsvalues)
        groupViewSets.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.nonhall.groups.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.nonhall.groups"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def normalTrainerPokemon(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 550
        width = 75

        label1 = ttk.Label(self.mainframe, text = tr("help.normal.trainer_pokemon.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        svalues = ["A1 w/ 3 IVs", "A1 w/ 3 IVs; B1 w/ 6 IVs", "B1 w/ 6 IVs; B2 w/ 9 IVs", "B2 w/ 9 IVs; C1 w/ 12 IVs", "C1 w/ 12 IVs; C2 w/ 15 IVs", "C2 w/ 15 IVs; C3 w/ 18 IVs", "C3 w/ 18 IVs; C4 w/ 21 IVs"]
        evalues = ["B1 w/ 6 IVs", "B2 w/ 9 IVs", tr("help.nonhall.trainer_pokemon.tree.silver"), "C2 w/ 15 IVs", "C3 w/ 18 IVs", "C4 w/ 21 IVs", tr("help.nonhall.trainer_pokemon.tree.gold")]
        streaks = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.trainer_pokemon.tree.groups"), svalues, evalues)
        streaks.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.normal.trainer_pokemon.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        values = [core.BattleNum.s99.value]
        depends = tr("help.normal.trainer_pokemon.tree.depends")
        colvalues = [f"C4 w/ 21 IVs; {depends} w/ 31 IVs"]
        streak50 = oneColTree(self.mainframe, width, tr("help.nonhall.trainer_pokemon.tree.battle"), tr("help.nonhall.trainer_pokemon.tree.groups"), values, colvalues)
        streak50.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.normal.trainer_pokemon"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def normalTrainerClasses(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 650
        width = 150

        label1 = ttk.Label(self.mainframe, text = tr("help.normal.trainer_classes.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        def typeNames(*indexes):
            names = [core.Type(i).name for i in indexes]
            return ", ".join(names)

        typeFrame = ttk.Frame(self.mainframe)
        typeFrame.columnconfigure(0, weight = 1)

        typeClasses = ["ace_trainer_f_snow", "ace_trainer_m_snow", "aroma_lady", "battle_girl", "black_belt", "bird_keeper", "bug_catcher", "cameraman", "clown", "cyclist_f", "cyclist_m", "fisherman", "hiker", "guitarist", "policeman", "psychic_f", "psychic_m", "roughneck", "ruin_maniac", "sailor", "tuber_f", "tuber_m", "worker"]
        values = [tr(f"trainer_class.{tclass}") for tclass in typeClasses]
        no_spec = tr("help.normal.trainer_classes.tree.no_spec")
        colsvalues = [[typeNames(0, 10, 14), typeNames(14)], [typeNames(0, 10, 14), typeNames(14)], [typeNames(0, 11), typeNames(11)], [no_spec, typeNames(1, 9)], [no_spec, typeNames(1, 9)], [typeNames(2), typeNames(2)], [typeNames(6, 11), "---"], [no_spec, typeNames(12, 13)], [no_spec, typeNames(7, 13)], [no_spec, typeNames(1, 2)], [no_spec, typeNames(1, 2)], [typeNames(10), typeNames(10)], [typeNames(1, 4, 5, 8), typeNames(4, 5)], [typeNames(1, 7, 12, 13, 16), typeNames(7, 12)], [typeNames(0, 1, 8), typeNames(1, 8)], [no_spec, typeNames(13)], [no_spec, typeNames(13)], [typeNames(1, 5, 7, 12, 16), typeNames(3, 7, 16)], [typeNames(4, 5, 8), typeNames(5, 8)], [typeNames(0, 1, 2, 10), typeNames(1, 10)], [typeNames(0, 10), "---"], [typeNames(0, 10), "---"], [typeNames(1, 4, 5), typeNames(4, 5)]]
        trainerView1 = multiColTree(typeFrame, width, tr("help.normal.trainer_classes.tree.class"), [tr("help.normal.trainer_classes.tree.type_spec.pre50"), tr("help.normal.trainer_classes.tree.type_spec.post50")], values, colsvalues)
        trainerView1.column('#0', width = 25)
        trainerView1.column(0, width = 80)
        trainerView1['height'] = 10

        scrollbar = ttk.Scrollbar(typeFrame, orient = 'vertical', command = trainerView1.yview)
        trainerView1['yscrollcommand'] = scrollbar.set

        trainerView1.grid(column = 0, row = 0, sticky = (W, N, E, S))
        scrollbar.grid(column = 1, row = 0, sticky = (W, N, E, S))

        typeFrame.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.normal.trainer_classes.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        specClasses = ["dragon_tamer", "idol", "pi"]
        values = [tr(f"trainer_class.{tclass}") for tclass in specClasses]
        colsvalues = [[tr("help.normal.trainer_classes.tree.spec.dragon_tamer"), tr("help.normal.trainer_classes.tree.spec.dragon_tamer")], [tr("help.normal.trainer_classes.tree.spec.pre50.idol"), tr("help.normal.trainer_classes.tree.spec.post50.idol")], [tr("help.normal.trainer_classes.tree.spec.pre50.pi"), tr("help.normal.trainer_classes.tree.spec.post50.pi")]]
        trainerView2 = multiColTree(self.mainframe, width, tr("help.normal.trainer_classes.tree.class"), [tr("help.normal.trainer_classes.tree.spec.pre50"), tr("help.normal.trainer_classes.tree.spec.post50")], values, colsvalues)
        trainerView2.column('#0', width = 20)
        trainerView2.column(0, width = 60)
        trainerView2.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.normal.trainer_classes"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def factoryTrainerPokemon50(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 550
        width = 75

        label1 = ttk.Label(self.mainframe, text = tr("help.factory.trainer_pokemon_50.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        svalues = ["A1 w/ 0 IVs", "A1 w/ 0 IVs; B1 w/ 4 IVs", "B1 w/ 4 IVs; B2 w/ 8 IVs", "B2 w/ 8 IVs; C1 w/ 12 IVs", "C1 w/ 12 IVs; C2 w/ 16 IVs", "C2 w/ 16 IVs; C3 w/ 20 IVs", "C3 w/ 20 IVs; C4 w/ 24 IVs"]
        evalues = ["B1 w/ 4 IVs", "B2 w/ 8 IVs", tr("help.nonhall.trainer_pokemon.tree.silver"), "C2 w/ 16 IVs", "C3 w/ 20 IVs", "C4 w/ 24 IVs", tr("help.nonhall.trainer_pokemon.tree.gold")]
        streaks = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.trainer_pokemon.tree.groups"), svalues, evalues)
        streaks.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.factory.trainer_pokemon_50.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        values = [core.BattleNum.s99.value]
        colvalues = ["C4 w/ 24 IVs; C/D w/ 31 IVs"]
        streak50 = oneColTree(self.mainframe, width, tr("help.nonhall.trainer_pokemon.tree.battle"), tr("help.nonhall.trainer_pokemon.tree.groups"), values, colvalues)
        streak50.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.factory.trainer_pokemon_50"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def factoryTrainerPokemonOpen(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 550
        width = 75

        label1 = ttk.Label(self.mainframe, text = tr("help.factory.trainer_pokemon_open.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        svalues = ["C1 w/ 0 IVs", "C1 w/ 0 IVs; C2 w/ 4 IVs", "C2 w/ 4 IVs; C3 w/ 8 IVs", "C3 w/ 8 IVs; C4 w/ 12 IVs", "C4 w/ 12 IVs; C/D w/ 16 IVs", "C/D w/ 16 IVs; C/D w/ 20 IVs", "C/D w/ 20 IVs; C/D w/ 24 IVs"]
        evalues = ["C2 w/ 4 IVs", "C3 w/ 8 IVs", tr("help.nonhall.trainer_pokemon.tree.silver"), "C/D w/ 16 IVs", "C/D w/ 20 IVs", "C/D w/ 24 IVs", tr("help.nonhall.trainer_pokemon.tree.gold")]
        streaks = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.trainer_pokemon.tree.groups"), svalues, evalues)
        streaks.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.factory.trainer_pokemon_open.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        values = [core.BattleNum.s99.value]
        colvalues = ["C/D w/ 24 IVs; C/D w/ 31 IVs"]
        streak50 = oneColTree(self.mainframe, width, tr("help.nonhall.trainer_pokemon.tree.battle"), tr("help.nonhall.trainer_pokemon.tree.groups"), values, colvalues)
        streak50.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.factory.trainer_pokemon_open"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallPokemon(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.hall.pokemon.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.nonhall.pokemon"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallGroups(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 250
        width = 50

        label = ttk.Label(self.mainframe, text = tr("help.hall.groups.info"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

        groupView = oneColTree(self.mainframe, width, tr("help.nonhall.groups.tree.name"), tr("help.nonhall.groups.tree.examples"))
        groupView['height'] = 4
        for hallsetgroup in core.HallSetGroup:
            groupView.insert('', 'end', text = hallsetgroup.fullname(), values = [tr(f"help.hall.groups.{hallsetgroup.name}.examples")])
        groupView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.nonhall.groups"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallRankPokemon(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.hall.rank_pokemon.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        values = []
        values.append(core.HallSetGroup.sub339.fullname())
        values.append(core.HallSetGroup.sub339.fullname())
        values.append(core.HallSetGroup.sub339.fullname() + ", " + core.HallSetGroup.from340to439.fullname())
        values.append(core.HallSetGroup.sub339.fullname() + ", " + core.HallSetGroup.from340to439.fullname())
        values.append(core.HallSetGroup.sub339.fullname() + ", " + core.HallSetGroup.from340to439.fullname())
        values.append(core.HallSetGroup.from340to439.fullname() + ", " + core.HallSetGroup.from440to499.fullname())
        values.append(core.HallSetGroup.from340to439.fullname() + ", " + core.HallSetGroup.from440to499.fullname())
        values.append(core.HallSetGroup.from340to439.fullname() + ", " + core.HallSetGroup.from440to499.fullname())
        values.append(core.HallSetGroup.from440to499.fullname() + ", " + core.HallSetGroup.plus500.fullname())
        values.append(core.HallSetGroup.from440to499.fullname() + ", " + core.HallSetGroup.plus500.fullname())
        rankGroups = makeRankTrees(self.mainframe, width, tr("help.hall.rank_pokemon.tree.groups"), values)
        rankGroups.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.hall.rank_pokemon.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        values = [tr("help.nonhall.trainer_pokemon.tree.silver"), tr("help.nonhall.trainer_pokemon.tree.gold")]
        colsvalues = [[50, tr("help.hall.rank_pokemon.tree.same")], [170, core.HallSetGroup.plus500.fullname()]]
        brainTree = multiColTree(self.mainframe, width, "", [tr("help.nonhall.trainer_pokemon.tree.battle"), tr("help.hall.rank_pokemon.tree.groups")], values, colsvalues)
        brainTree.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.hall.rank_pokemon"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallRankIVs(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.hall.rank_ivs.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        rankIVs = makeRankTrees(self.mainframe, width, tr("help.hall.rank_ivs.tree.ivs"), range(8, 28, 2))
        rankIVs.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.hall.rank_ivs.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.hall.rank_ivs"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallLevel(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.hall.level.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.hall.level"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsArcadeBoard(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 500
        width = 100
        style = "ArcadeIcons.Treeview"
        ttk.Style().configure(style, rowheight = 28) # height of arcade icons

        label1 = ttk.Label(self.mainframe, text = tr("help.mechanics.arcade.board.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        def trEvent(event):
            return tr(f"help.mechanics.arcade.board.tree.{event}")
        def iconEvent(event):
            return PhotoImage(file = "gui/arcade icons/" + event + ".png")

        colorframe = ttk.Frame(self.mainframe)
        colorframe.columnconfigure(0, weight = 1)
        colorframe.columnconfigure(1, weight = 2)

        targetedEvents = ["poison", "paralyze", "burn", "sleep", "freeze", "berry", "item", "lower_hp", "level_up"]
        targetedDescs = [trEvent(event) for event in targetedEvents]
        self.targetedIcons = [iconEvent(event) for event in targetedEvents]

        boardView1 = makeIconTree(colorframe, width, targetedDescs[0:5], self.targetedIcons[0:5], style)
        boardView1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        boardView2 = makeIconTree(colorframe, width, targetedDescs[5:], self.targetedIcons[5:], style)
        boardView2.grid(column = 1, row = 0, sticky = (W, N, E, S))

        colorframe.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.mechanics.arcade.board.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        grayframe = ttk.Frame(self.mainframe)
        grayframe.columnconfigure(0, weight = 1)
        grayframe.columnconfigure(1, weight = 2)

        fieldEvents = ["no_event", "sun", "rain", "sandstorm", "hail", "fog", "trick_room", "speed_up", "speed_down", "random", "pass", "bp", "bp_plus", "swap_teams"]
        fieldDescs = [trEvent(event) for event in fieldEvents]
        self.fieldIcons = [iconEvent(event) for event in fieldEvents]

        boardView3 = makeIconTree(grayframe, width, fieldDescs[0:7], self.fieldIcons[0:7], style)
        boardView3.grid(column = 0, row = 0, sticky = (W, N, E, S))

        boardView4 = makeIconTree(grayframe, width, fieldDescs[7:], self.fieldIcons[7:], style)
        boardView4.grid(column = 1, row = 0, sticky = (W, N, E, S))

        grayframe.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.mechanics.arcade.board.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.mechanics.arcade.board"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsCastleEarn(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 400

        label = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.earning_points.info"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

        values = [3, 3, 2, 1, 1, 8, 6, 4, 7]
        conditions = ["not_fainted", "full_hp", "more_than_half_hp", "less_than_half_hp", "no_status", "5_pp", "10_pp", "15_pp", "leveled_up"]
        colvalues = [tr(f"help.mechanics.castle.earning_points.tree.{condition}") for condition in conditions]
        earnView = oneColTree(self.mainframe, 50, tr("help.mechanics.castle.earning_points.tree.earned"), tr("help.mechanics.castle.earning_points.tree.condition"), values, colvalues)
        earnView.column('col', width = 250)
        earnView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.mechanics.castle.earning_points"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsCastleSpend(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 75

        label1 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        infoView = makeSpendTree(self.mainframe, width, 6, [100, 100], [[("hp", 10)], [("pp", 8)], [("hppp", 12)]])
        infoView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        infoView = makeSpendTree(self.mainframe, width, 7, [50], [[("identify", 1), ("stats", 2), ("level_up", 1), ("level_down", 15)], [("moves", 5)]])
        infoView.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

        passView = oneColTree(self.mainframe, width, tr("help.mechanics.castle.spending_points.tree.option"), tr("help.mechanics.castle.spending_points.tree.cost"), [tr("help.mechanics.castle.spending_points.tree.pass")], [50])
        passView.column('col', width = 25)
        passView.grid(column = 0, row = 5, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.mechanics.castle.spending_points"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsCastleSpendItems(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450

        label1 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.items.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        itemViewFrame = ttk.Frame(self.mainframe)
        itemViewFrame.columnconfigure(0, weight = 1)

        itemView = oneColTree(itemViewFrame, 250, tr("help.mechanics.castle.spending_points.tree.option"), tr("help.mechanics.castle.spending_points.tree.cost"))
        itemView['height'] = 15
        itemView.column('col', width = 50)

        def insertItemCosts(level, value, *items):
            for item in items:
                itemView.insert(level, 'end', text = tr(f"item.{item}"), values = [value])

        # level 1
        level = itemView.insert('', 'end', text = tr("help.mechanics.castle.spending_points.tree.unlock.1"), values = ["---"], open = True)
        sublevel = itemView.insert(level, 'end', text = tr("help.mechanics.castle.spending_points.items.tree.status_berries"), values = [2])
        insertItemCosts(sublevel, 2, "cheri_berry", "chesto_berry", "pecha_berry", "rawst_berry", "aspear_berry", "persim_berry")
        insertItemCosts(level, 5, "lum_berry", "sitrus_berry")
        # level 2
        level = itemView.insert('', 'end', text = tr("help.mechanics.castle.spending_points.tree.unlock.2"), values = [100], open = True)
        insertItemCosts(level, 5, "power_herb")
        insertItemCosts(level, 10, "kings_rock", "metronome", "light_clay", "grip_claw", "big_root", "toxic_orb", "flame_orb")
        insertItemCosts(level, 15, "quick_claw", "shell_bell", "light_ball", "thick_club")
        # level 3
        level = itemView.insert('', 'end', text = tr("help.mechanics.castle.spending_points.tree.unlock.3"), values = [150], open = True)
        insertItemCosts(level, 5, "white_herb")
        insertItemCosts(level, 10, "focus_sash")
        insertItemCosts(level, 15, "focus_band")
        insertItemCosts(level, 20, "leftovers", "bright_powder", "scope_lens", "wide_lens", "zoom_lens", "choice_band", "choice_specs", "choice_scarf", "muscle_band", "wise_glasses", "expert_belt", "life_orb")
        sublevel = itemView.insert(level, 'end', text = tr("help.mechanics.castle.spending_points.items.tree.stat_pinch_berries"), values = [5])
        insertItemCosts(sublevel, 5, "liechi_berry", "ganlon_berry", "salac_berry", "petaya_berry", "apicot_berry", "lansat_berry", "starf_berry")
        sublevel = itemView.insert(level, 'end', text = tr("help.mechanics.castle.spending_points.items.tree.damage_reducing_berries"), values = [5])
        insertItemCosts(sublevel, 5, "occa_berry", "passho_berry", "wacan_berry", "rindo_berry", "yache_berry", "chople_berry", "kebia_berry", "shuca_berry", "coba_berry", "payapa_berry", "tanga_berry", "charti_berry", "kasib_berry", "haban_berry", "colbur_berry", "babiri_berry", "chilan_berry")

        scrollbar = ttk.Scrollbar(itemViewFrame, orient = 'vertical', command = itemView.yview)
        itemView['yscrollcommand'] = scrollbar.set

        itemView.grid(column = 0, row = 0, sticky = (W, N, E, S))
        scrollbar.grid(column = 1, row = 0, sticky = (W, N, E, S))

        itemViewFrame.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.mechanics.castle.spending_points.items"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsFactoryRentals(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.mechanics.factory.starting_rentals.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        values = [1, 2, 3, 4, 5, 6, 7, "8+"]
        colsvalues = [["A1 w/ 0 IVs", "C1 w/ 0 IVs"], ["B1 w/ 4 IVs", "C2 w/ 4 IVs"], ["B2 w/ 8 IVs", "C3 w/ 8 IVs"], ["C1 w/ 12 IVs", "C4 w/ 12 IVs"], ["C2 w/ 16 IVs", "C/D w/ 16 IVs"], ["C3 w/ 20 IVs", "C/D w/ 20 IVs"], ["C4 w/ 24 IVs", "C/D w/ 24 IVs"], ["C/D w/ 31 IVs", "C/D w/ 31 IVs"]]
        starting = multiColTree(self.mainframe, width, tr("help.mechanics.factory.starting_rentals.round"), [tr("help.mechanics.factory.starting_rentals.50"), tr("help.mechanics.factory.starting_rentals.open")], values, colsvalues)
        #starting.column('#0', width = 25)
        starting.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.mechanics.factory.starting_rentals.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.mechanics.factory.starting_rentals"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsFactoryClauses(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.mechanics.factory.clauses.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.mechanics.factory.clauses"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()



def oneColTree(parent, width, name, heading, values = [], colvalues = []):
    tree = ttk.Treeview(parent, height = len(values), columns = ('col'), takefocus = 0)
    tree.heading('#0', text = name)
    tree.column('#0', width = width)
    tree.heading('col', text = heading)
    tree.column('col', width = width)
    for value, colvalue in zip(values, colvalues):
        tree.insert('', 'end', text = value, values = [colvalue])
    return tree

def multiColTree(parent, width, name, headings, values = [], colsvalues = []):
    tree = ttk.Treeview(parent, height = len(values), columns = range(len(headings)), takefocus = 0)
    tree.heading('#0', text = name)
    tree.column('#0', width = width)
    for colnum, heading in enumerate(headings):
        tree.heading(colnum, text = heading)
        tree.column(colnum, width = width)
    for value, colvalues in zip(values, colsvalues):
        tree.insert('', 'end', text = value, values = colvalues)
    return tree

def noColTree(parent, width, name, values = []):
    tree = ttk.Treeview(parent, height = len(values), takefocus = 0)
    tree.heading('#0', text = name)
    tree.column('#0', width = width)
    for value in values:
        tree.insert('', 'end', text = value)
    return tree

# returns a frame with two treeviews next to each other containg the values for the battlenums
def makeBattleNumTrees(parent, width, heading, svalues, evalues):

    frame = ttk.Frame(parent)
    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight = 1)

    values = [core.BattleNum.s1.value, core.BattleNum.s2.value, core.BattleNum.s3.value, core.BattleNum.s4.value, core.BattleNum.s5.value, core.BattleNum.s6.value, core.BattleNum.s7.value]
    if len(svalues) > 7:
        values.append(core.BattleNum.s99.value)
    treeS = oneColTree(frame, width, tr("help.nonhall.trainer_pokemon.tree.battle"), heading, values, svalues)
    treeS.column('#0', width = 25)
    treeS.grid(column = 0, row = 0, sticky = (W, N, E, S))

    values = [core.BattleNum.e1.value, core.BattleNum.e2.value, core.BattleNum.e3.value, core.BattleNum.e4.value, core.BattleNum.e5.value, core.BattleNum.e6.value, core.BattleNum.e7.value]
    treeE = oneColTree(frame, width, tr("help.nonhall.trainer_pokemon.tree.battle.ender"), heading, values, evalues)
    treeE.column('#0', width = 25)
    treeE.grid(column = 1, row = 0, sticky = (W, N, E, S))

    return frame

# returns a frame with two treeviews next to each other containg the values for the ranks
def makeRankTrees(parent, width, heading, values):

    frame = ttk.Frame(parent)
    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight = 1)

    tree1 = oneColTree(frame, width, tr("help.hall.rank_pokemon.tree.rank"), heading, range(1, 6), values[0:5])
    tree1.grid(column = 0, row = 0, sticky = (W, N, E, S))

    tree2 = oneColTree(frame, width, tr("help.hall.rank_pokemon.tree.rank"), heading, range(6, 11), values[5:])
    tree2.grid(column = 1, row = 0, sticky = (W, N, E, S))

    return frame

# returns a tree containing levels and costs and values for castle points
def makeSpendTree(parent, width, height, level_costs, level_values):

    tree = oneColTree(parent, width, tr("help.mechanics.castle.spending_points.tree.option"), tr("help.mechanics.castle.spending_points.tree.cost"))
    tree['height'] = height
    tree.column('col', width = 25)
    level_ids = []
    level_ids.append(tree.insert('', 'end', text = tr("help.mechanics.castle.spending_points.tree.unlock.1"), values = ["---"], open = True))
    for level, cost in enumerate(level_costs, start = 2):
        level_ids.append(tree.insert('', 'end', text = tr(f"help.mechanics.castle.spending_points.tree.unlock.{level}"), values = [cost], open = True))
    for level, values in enumerate(level_values):
        for option, cost in values:
            tree.insert(level_ids[level], 'end', text = tr(f"help.mechanics.castle.spending_points.tree.{option}"), values = [cost])

    return tree

# returns a tree with the icons and descriptions and no headings
def makeIconTree(parent, width, descs, icons, style):

    tree = ttk.Treeview(parent, height = len(descs), takefocus = 0, show = 'tree', style = style)
    tree.column('#0', width = width)
    for desc, icon in zip(descs, icons):
        tree.insert('', 'end', text = desc, image = icon)

    return tree
