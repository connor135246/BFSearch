# helpdialogs


from tkinter import *
from tkinter import ttk

from bfsearch import core
from bfsearch.translate import tr
from bfsearch.tkinter import dialogs



# general dialogs

def mainHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.basics"), basicHelp))
    helpoptions.append((tr("help.nonhall"), nonhallHelp))
    helpoptions.append((tr("help.hall"), hallHelp))
    helpoptions.append((tr("help.mechanics"), mechanicsHelp))
    HelpDialog(parent, tr("toolbar.button.help.name"), tr("help"), helpoptions).show()
    parent.grab_set()

def nonhallHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), nonhallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), nonhallGroups))
    helpoptions.append((tr("help.nonhall.streaks"), nonhallStreaks))
    helpoptions.append((tr("help.nonhall.trainers"), nonhallTrainers))
    HelpDialog(parent, tr("help.nonhall"), tr("help"), helpoptions).show()
    parent.grab_set()

def hallHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.nonhall.pokemon"), hallPokemon))
    helpoptions.append((tr("help.nonhall.groups"), hallGroups))
    helpoptions.append((tr("help.hall.rank"), hallRank))
    helpoptions.append((tr("help.hall.level"), hallLevel))
    HelpDialog(parent, tr("help.hall"), tr("help"), helpoptions).show()
    parent.grab_set()

def mechanicsHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.mechanics.arcade.roulette"), mechanicsArcadeRoulette))
    helpoptions.append((tr("help.mechanics.castle.earning_points"), mechanicsCastleEarn))
    helpoptions.append((tr("help.mechanics.castle.spending_points"), mechanicsCastleSpend))
    helpoptions.append((tr("help.mechanics.factory.swapping"), mechanicsFactorySwap))
    helpoptions.append((tr("help.mechanics.factory.clauses"), mechanicsFactoryClauses))
    HelpDialog(parent, tr("help.mechanics"), tr("help"), helpoptions).show()
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

        groupView = ttk.Treeview(self.mainframe, height = 4, columns = ('desc', 'examples'), takefocus = 0)
        groupView.heading('#0', text = tr("help.nonhall.groups.tree.name"))
        groupView.column('#0', width = width)
        groupView.heading('desc', text = tr("help.nonhall.groups.tree.desc"))
        groupView.column('desc', width = width)
        groupView.heading('examples', text = tr("help.nonhall.groups.tree.examples"))
        groupView.column('examples', width = width)
        for group in ['a', 'b', 'c', 'd']:
            groupView.insert('', 'end', text = tr(f"help.nonhall.groups.{group}.name"), values = (tr(f"help.nonhall.groups.{group}.desc"), tr(f"help.nonhall.groups.{group}.examples")))
        groupView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.nonhall.groups.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        groupViewSets = ttk.Treeview(self.mainframe, height = 4, columns = ('sets', 'subs'), takefocus = 0)
        groupViewSets.heading('#0', text = tr("help.nonhall.groups.tree.name"))
        groupViewSets.column('#0', width = width)
        groupViewSets.heading('sets', text = tr("help.nonhall.groups.tree.sets"))
        groupViewSets.column('sets', width = width)
        groupViewSets.heading('subs', text = tr("help.nonhall.groups.tree.subs"))
        groupViewSets.column('subs', width = width)
        for group in ['a', 'b', 'c', 'd']:
            groupViewSets.insert('', 'end', text = tr(f"help.nonhall.groups.{group}.name"), values = (tr(f"help.nonhall.groups.{group}.sets"), tr(f"help.nonhall.groups.{group}.subs")))
        groupViewSets.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.nonhall.groups.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.nonhall.groups"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def nonhallStreaks(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 550
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.nonhall.streaks.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        svalues = ["A1", "A1, B1", "B1, B2", "B2, C1", "C1, C2", "C2, C3", "C3, C4"]
        evalues = ["B1", "B2", tr("help.nonhall.streaks.tree.brain"), "C2", "C3", "C4", tr("help.nonhall.streaks.tree.brain")]
        streaks = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.streaks.tree.groups"), svalues, evalues)
        streaks.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.nonhall.streaks.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        values = [core.BattleNum.s99.value + " " + tr("help.nonhall.streaks.tree.normal"), core.BattleNum.s99.value + " " + tr("help.nonhall.streaks.tree.factory")]
        colvalues = ["B2, C1-C4, D1-D4", "C1-C4, D1-D4"]
        streak50 = oneColTree(self.mainframe, width, tr("help.nonhall.streaks.tree.battle"), tr("help.nonhall.streaks.tree.groups"), values, colvalues)
        streak50.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.nonhall.streaks.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

        svalues = ["C1", "C1, C2", "C2, C3", "C3, C4", "C1-C4, D1-D4", "C1-C4, D1-D4", "C1-C4, D1-D4"]
        evalues = ["C2", "C3", tr("help.nonhall.streaks.tree.brain"), "C1-C4, D1-D4", "C1-C4, D1-D4", "C1-C4, D1-D4", tr("help.nonhall.streaks.tree.brain")]
        streaksOpen = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.streaks.tree.groups"), svalues, evalues)
        streaksOpen.grid(column = 0, row = 5, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.nonhall.streaks"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def nonhallTrainers(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 550
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.nonhall.trainers.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        svalues = ["3", "3, 6", "6, 9", "9, 12", "12, 15", "15, 18", "18, 21", "21, 31"]
        evalues = ["6", "9", tr("help.nonhall.trainers.tree.brain"), "15", "18", "21", tr("help.nonhall.trainers.tree.brain")]
        ivs = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.trainers.tree.ivs"), svalues, evalues)
        ivs.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.nonhall.trainers.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        svalues = ["0", "0, 4", "4, 8", "8, 12", "12, 16", "16, 20", "20, 24", "24, 31"]
        evalues = ["4", "8", tr("help.nonhall.trainers.tree.brain"), "16", "20", "24", tr("help.nonhall.trainers.tree.brain")]
        ivsFactory = makeBattleNumTrees(self.mainframe, width, tr("help.nonhall.trainers.tree.ivs"), svalues, evalues)
        ivsFactory.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.nonhall.trainers"), [tr("toolbar.button.ok")], builder).show()
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
        for hallsetgroup in list(core.HallSetGroup):
            groupView.insert('', 'end', text = hallsetgroup.fullname(), values = [tr(f"help.hall.groups.{hallsetgroup.name}.examples")])
        groupView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.nonhall.groups"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallRank(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 50

        label1 = ttk.Label(self.mainframe, text = tr("help.hall.rank.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
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
        tree = makeRankTrees(self.mainframe, width, tr("help.nonhall.streaks.tree.groups"), values)
        tree.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.hall.rank.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        tree = makeRankTrees(self.mainframe, width, tr("help.hall.rank.tree.ivs"), range(8, 28, 2))
        tree.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.hall.rank.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.hall.rank"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def hallLevel(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.hall.level.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.hall.level"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsArcadeRoulette(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450
        width = 100

        label = ttk.Label(self.mainframe, text = tr("help.mechanics.arcade.roulette.info"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

        def trEffect(effect):
            return tr(f"help.mechanics.arcade.roulette.tree.{effect}")

        values = list(map(trEffect, ["lower_hp", "poison", "paralyze", "burn", "sleep", "freeze", "berry", "item", "level_up"]))
        rouletteView1 = noColTree(self.mainframe, width, tr("help.mechanics.arcade.roulette.tree.targeted"), values)
        rouletteView1.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        values = list(map(trEffect, ["sun", "rain", "sandstorm", "hail", "fog", "trick_room"]))
        rouletteView2 = noColTree(self.mainframe, width, tr("help.mechanics.arcade.roulette.tree.field"), values)
        rouletteView2.grid(column = 0, row = 2, sticky = (W, N, E, S), padx = 10, pady = 5)

        values = list(map(trEffect, ["nothing", "swap", "skip", "get_1", "get_3", "speed_up", "speed_down", "random"]))
        rouletteView3 = noColTree(self.mainframe, width, tr("help.mechanics.arcade.roulette.tree.other"), values)
        rouletteView3.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.mechanics.arcade.roulette"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsCastleEarn(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 350

        label = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.earning_points.info"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

        values = [3, 3, 2, 1, 1, 8, 6, 4, 7]
        conditions = ["not_fainted", "full_hp", "more_than_half_hp", "less_than_half_hp", "no_status", "under_5_pp", "under_10_pp", "under_15_pp", "leveled_up"]
        colvalues = list(map(lambda condition: tr(f"help.mechanics.castle.earning_points.tree.{condition}"), conditions))
        earnView = oneColTree(self.mainframe, 50, tr("help.mechanics.castle.earning_points.tree.earned"), tr("help.mechanics.castle.earning_points.tree.condition"), values, colvalues)
        earnView.column('col', width = 250)
        earnView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.mechanics.castle.earning_points"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def mechanicsCastleSpend(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 400
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

        passView = oneColTree(self.mainframe, width, tr("help.mechanics.castle.spending_points.tree.feature"), tr("help.mechanics.castle.spending_points.tree.cost"), [tr(f"help.mechanics.castle.spending_points.tree.pass")], [50])
        passView.column('col', width = 25)
        passView.grid(column = 0, row = 5, sticky = (W, N, E, S), padx = 10, pady = 5)

        label4 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.info.4"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label4.grid(column = 0, row = 6, sticky = (W, N, E, S))

    pressed = dialogs.CustomDialog(parent, tr("help.mechanics.castle.spending_points"), [tr("toolbar.button.next"), tr("toolbar.button.ok")], builder).show()
    if pressed == 0:
        parent._root().after_idle(mechanicsCastleSpendItems, parent)
    parent.grab_set()

def mechanicsCastleSpendItems(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450

        label1 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.items.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        itemViewFrame = ttk.Frame(self.mainframe)
        itemViewFrame.columnconfigure(0, weight = 1)

        itemView = oneColTree(itemViewFrame, 250, tr("help.mechanics.castle.spending_points.tree.feature"), tr("help.mechanics.castle.spending_points.tree.cost"))
        itemView['height'] = 20
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

        label2 = ttk.Label(self.mainframe, text = tr("help.mechanics.castle.spending_points.items.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

    pressed = dialogs.CustomDialog(parent, tr("help.mechanics.castle.spending_points.items"), [tr("toolbar.button.prev"), tr("toolbar.button.ok")], builder).show()
    if pressed == 0:
        parent._root().after_idle(mechanicsCastleSpend, parent)
    parent.grab_set()

def mechanicsFactorySwap(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.mechanics.factory.swapping.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.mechanics.factory.swapping"), [tr("toolbar.button.ok")], builder).show()
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
    treeS = oneColTree(frame, width, tr("help.nonhall.streaks.tree.battle"), heading, values, svalues)
    treeS.grid(column = 0, row = 0, sticky = (W, N, E, S))

    values = [core.BattleNum.e1.value, core.BattleNum.e2.value, core.BattleNum.e3.value, core.BattleNum.e4.value, core.BattleNum.e5.value, core.BattleNum.e6.value, core.BattleNum.e7.value]
    treeE = oneColTree(frame, width, tr("help.nonhall.streaks.tree.battle.ender"), heading, values, evalues)
    treeE.grid(column = 1, row = 0, sticky = (W, N, E, S))

    return frame

# returns a frame with two treeviews next to each other containg the values for the ranks
def makeRankTrees(parent, width, heading, values):

    frame = ttk.Frame(parent)
    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight = 1)

    tree1 = oneColTree(frame, width, tr("help.hall.rank.tree.rank"), heading, range(1, 6), values[0:5])
    tree1.grid(column = 0, row = 0, sticky = (W, N, E, S))

    tree2 = oneColTree(frame, width, tr("help.hall.rank.tree.rank"), heading, range(6, 11), values[5:])
    tree2.grid(column = 1, row = 0, sticky = (W, N, E, S))

    return frame

# returns a tree containing levels and costs and values for castle points
def makeSpendTree(parent, width, height, level_costs, level_values):

    tree = oneColTree(parent, width, tr("help.mechanics.castle.spending_points.tree.feature"), tr("help.mechanics.castle.spending_points.tree.cost"))
    tree['height'] = height
    tree.column('col', width = 25)
    level_ids = []
    level_ids.append(tree.insert('', 'end', text = tr("help.mechanics.castle.spending_points.tree.unlock.1"), values = ["---"], open = True))
    for level, cost in enumerate(level_costs, start = 2):
        level_ids.append(tree.insert('', 'end', text = tr(f"help.mechanics.castle.spending_points.tree.unlock.{level}"), values = [cost], open = True))
    for level, values in enumerate(level_values):
        for feature, cost in values:
            tree.insert(level_ids[level], 'end', text = tr(f"help.mechanics.castle.spending_points.tree.{feature}"), values = [cost])

    return tree
