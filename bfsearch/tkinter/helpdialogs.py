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
    helpoptions.append((tr("help.tricks"), tricksHelp))
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

def tricksHelp(parent):
    helpoptions = []
    helpoptions.append((tr("help.tricks.castle.earning_points"), tricksCastleEarn))
    helpoptions.append((tr("help.tricks.castle.spending_points"), tricksCastleSpend))
    helpoptions.append((tr("help.tricks.factory.swapping"), tricksFactorySwap))
    helpoptions.append((tr("help.tricks.factory.clauses"), tricksFactoryClauses))
    HelpDialog(parent, tr("help.tricks"), tr("help"), helpoptions).show()
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

        streak50 = ttk.Treeview(self.mainframe, height = 2, columns = ('groups'), takefocus = 0)
        streak50.heading('#0', text = tr("help.nonhall.streaks.tree.battle"))
        streak50.column('#0', width = width)
        streak50.heading('groups', text = tr("help.nonhall.streaks.tree.groups"))
        streak50.column('groups', width = width)
        streak50.insert('', 'end', text = f"{core.BattleNum.s99.value} [Tower/Arcade/Castle]", values = ["B2, C1-C4, D1-D4"])
        streak50.insert('', 'end', text = f"{core.BattleNum.s99.value} [Factory]", values = ["C1-C4, D1-D4"])
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

        groupView = ttk.Treeview(self.mainframe, height = 4, columns = ('examples'), takefocus = 0)
        groupView.heading('#0', text = tr("help.nonhall.groups.tree.name"))
        groupView.column('#0', width = width)
        groupView.heading('examples', text = tr("help.nonhall.groups.tree.examples"))
        groupView.column('examples', width = width)
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
        values.append([core.HallSetGroup.sub339.fullname()])
        values.append([core.HallSetGroup.sub339.fullname()])
        values.append([core.HallSetGroup.sub339.fullname() + ", " + core.HallSetGroup.from340to439.fullname()])
        values.append([core.HallSetGroup.sub339.fullname() + ", " + core.HallSetGroup.from340to439.fullname()])
        values.append([core.HallSetGroup.sub339.fullname() + ", " + core.HallSetGroup.from340to439.fullname()])
        values.append([core.HallSetGroup.from340to439.fullname() + ", " + core.HallSetGroup.from440to499.fullname()])
        values.append([core.HallSetGroup.from340to439.fullname() + ", " + core.HallSetGroup.from440to499.fullname()])
        values.append([core.HallSetGroup.from340to439.fullname() + ", " + core.HallSetGroup.from440to499.fullname()])
        values.append([core.HallSetGroup.from440to499.fullname() + ", " + core.HallSetGroup.plus500.fullname()])
        values.append([core.HallSetGroup.from440to499.fullname() + ", " + core.HallSetGroup.plus500.fullname()])
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

def tricksCastleEarn(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 350

        label = ttk.Label(self.mainframe, text = tr("help.tricks.castle.earning_points.info"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

        earnView = ttk.Treeview(self.mainframe, height = 9, columns = ('earned'), takefocus = 0)
        earnView.heading('#0', text = tr("help.tricks.castle.earning_points.tree.earned"))
        earnView.column('#0', width = 50)
        earnView.heading('earned', text = tr("help.tricks.castle.earning_points.tree.condition"))
        earnView.column('earned', width = 250)
        conditions = [("not_fainted", 3), ("full_hp", 3), ("more_than_half_hp", 2), ("less_than_half_hp", 1), ("no_status", 1), ("under_5_pp", 8), ("under_10_pp", 6), ("under_15_pp", 4), ("leveled_up", 7)]
        for condition, earned in conditions:
            earnView.insert('', 'end', text = earned, values = [tr(f"help.tricks.castle.earning_points.tree.{condition}")])
        earnView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

    dialogs.CustomDialog(parent, tr("help.tricks.castle.earning_points"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def tricksCastleSpend(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 400
        width = 75

        label1 = ttk.Label(self.mainframe, text = tr("help.tricks.castle.spending_points.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        infoView = makeSpendTree(self.mainframe, width, 6, [100, 100], [[("hp", 10)], [("pp", 8)], [("hppp", 12)]])
        infoView.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.tricks.castle.spending_points.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

        infoView = makeSpendTree(self.mainframe, width, 7, [50], [[("identify", 1), ("stats", 2), ("level_up", 1), ("level_down", 15)], [("moves", 5)]])
        infoView.grid(column = 0, row = 3, sticky = (W, N, E, S), padx = 10, pady = 5)

        label3 = ttk.Label(self.mainframe, text = tr("help.tricks.castle.spending_points.info.3"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label3.grid(column = 0, row = 4, sticky = (W, N, E, S))

        passView = ttk.Treeview(self.mainframe, height = 1, columns = ('cost'), takefocus = 0)
        passView.heading('#0', text = tr("help.tricks.castle.spending_points.tree.feature"))
        passView.column('#0', width = width)
        passView.heading('cost', text = tr("help.tricks.castle.spending_points.tree.cost"))
        passView.column('cost', width = 25)
        passView.insert('', 'end', text = tr(f"help.tricks.castle.spending_points.tree.pass"), values = [50])
        passView.grid(column = 0, row = 5, sticky = (W, N, E, S), padx = 10, pady = 5)

        label4 = ttk.Label(self.mainframe, text = tr("help.tricks.castle.spending_points.info.4"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label4.grid(column = 0, row = 6, sticky = (W, N, E, S))

    pressed = dialogs.CustomDialog(parent, tr("help.tricks.castle.spending_points"), [tr("toolbar.button.next"), tr("toolbar.button.ok")], builder).show()
    if pressed == 0:
        parent._root().after_idle(tricksCastleSpendItems, parent)
    parent.grab_set()

def tricksCastleSpendItems(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)
        wraplength = 450

        label1 = ttk.Label(self.mainframe, text = tr("help.tricks.castle.spending_points.items.info.1"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label1.grid(column = 0, row = 0, sticky = (W, N, E, S))

        itemViewFrame = ttk.Frame(self.mainframe)
        itemViewFrame.columnconfigure(0, weight = 1)

        itemView = ttk.Treeview(itemViewFrame, height = 20, columns = ('cost'), takefocus = 0)
        itemView.heading('#0', text = tr("help.tricks.castle.spending_points.tree.feature"))
        itemView.column('#0', width = 250)
        itemView.heading('cost', text = tr("help.tricks.castle.spending_points.tree.cost"))
        itemView.column('cost', width = 50)

        def insertItemCosts(level, value, *items):
            for item in items:
                itemView.insert(level, 'end', text = tr(f"item.{item}"), values = [value])

        # level 1
        level = itemView.insert('', 'end', text = tr("help.tricks.castle.spending_points.tree.unlock.1"), values = ["---"], open = True)
        sublevel = itemView.insert(level, 'end', text = tr("help.tricks.castle.spending_points.items.tree.status_berries"), values = [2])
        insertItemCosts(sublevel, 2, "cheri_berry", "chesto_berry", "pecha_berry", "rawst_berry", "aspear_berry", "persim_berry")
        insertItemCosts(level, 5, "lum_berry", "sitrus_berry")
        # level 2
        level = itemView.insert('', 'end', text = tr("help.tricks.castle.spending_points.tree.unlock.2"), values = [100], open = True)
        insertItemCosts(level, 5, "power_herb")
        insertItemCosts(level, 10, "kings_rock", "metronome", "light_clay", "grip_claw", "big_root", "toxic_orb", "flame_orb")
        insertItemCosts(level, 15, "quick_claw", "shell_bell", "light_ball", "thick_club")
        # level 3
        level = itemView.insert('', 'end', text = tr("help.tricks.castle.spending_points.tree.unlock.3"), values = [150], open = True)
        insertItemCosts(level, 5, "white_herb")
        insertItemCosts(level, 10, "focus_sash")
        insertItemCosts(level, 15, "focus_band")
        insertItemCosts(level, 20, "leftovers", "bright_powder", "scope_lens", "wide_lens", "zoom_lens", "choice_band", "choice_specs", "choice_scarf", "muscle_band", "wise_glasses", "expert_belt", "life_orb")
        sublevel = itemView.insert(level, 'end', text = tr("help.tricks.castle.spending_points.items.tree.stat_pinch_berries"), values = [5])
        insertItemCosts(sublevel, 5, "liechi_berry", "ganlon_berry", "salac_berry", "petaya_berry", "apicot_berry", "lansat_berry", "starf_berry")
        sublevel = itemView.insert(level, 'end', text = tr("help.tricks.castle.spending_points.items.tree.damage_reducing_berries"), values = [5])
        insertItemCosts(sublevel, 5, "occa_berry", "passho_berry", "wacan_berry", "rindo_berry", "yache_berry", "chople_berry", "kebia_berry", "shuca_berry", "coba_berry", "payapa_berry", "tanga_berry", "charti_berry", "kasib_berry", "haban_berry", "colbur_berry", "babiri_berry", "chilan_berry")

        scrollbar = ttk.Scrollbar(itemViewFrame, orient = 'vertical', command = itemView.yview)
        itemView['yscrollcommand'] = scrollbar.set

        itemView.grid(column = 0, row = 0, sticky = (W, N, E, S))
        scrollbar.grid(column = 1, row = 0, sticky = (W, N, E, S))

        itemViewFrame.grid(column = 0, row = 1, sticky = (W, N, E, S), padx = 10, pady = 5)

        label2 = ttk.Label(self.mainframe, text = tr("help.tricks.castle.spending_points.items.info.2"), wraplength = wraplength, padding = (10, 5, 10, 5))
        label2.grid(column = 0, row = 2, sticky = (W, N, E, S))

    pressed = dialogs.CustomDialog(parent, tr("help.tricks.castle.spending_points.items"), [tr("toolbar.button.prev"), tr("toolbar.button.ok")], builder).show()
    if pressed == 0:
        parent._root().after_idle(tricksCastleSpend, parent)
    parent.grab_set()

def tricksFactorySwap(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.tricks.factory.swapping.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.tricks.factory.swapping"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()

def tricksFactoryClauses(parent):
    def builder(self, **kwargs):
        self.mainframe.columnconfigure(0, weight = 1)

        label = ttk.Label(self.mainframe, text = tr("help.tricks.factory.clauses.info"), wraplength = 450, padding = (10, 5, 10, 5))
        label.grid(column = 0, row = 0, sticky = (W, N, E, S))

    dialogs.CustomDialog(parent, tr("help.tricks.factory.clauses"), [tr("toolbar.button.ok")], builder).show()
    parent.grab_set()



# returns a frame with two treeviews next to each other containg the values for the battlenums
def makeBattleNumTrees(parent, width, heading, svalues, evalues):

    include50 = len(svalues) > 7

    frame = ttk.Frame(parent)
    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight = 1) 

    treeS = ttk.Treeview(frame, height = 8 if include50 else 7, columns = ('col'), takefocus = 0)
    treeS.heading('#0', text = tr("help.nonhall.streaks.tree.battle"))
    treeS.column('#0', width = width)
    treeS.heading('col', text = heading)
    treeS.column('col', width = width)
    treeS.insert('', 'end', text = core.BattleNum.s1.value, values = [svalues[0]])
    treeS.insert('', 'end', text = core.BattleNum.s2.value, values = [svalues[1]])
    treeS.insert('', 'end', text = core.BattleNum.s3.value, values = [svalues[2]])
    treeS.insert('', 'end', text = core.BattleNum.s4.value, values = [svalues[3]])
    treeS.insert('', 'end', text = core.BattleNum.s5.value, values = [svalues[4]])
    treeS.insert('', 'end', text = core.BattleNum.s6.value, values = [svalues[5]])
    treeS.insert('', 'end', text = core.BattleNum.s7.value, values = [svalues[6]])
    if include50:
        treeS.insert('', 'end', text = core.BattleNum.s99.value, values = [svalues[7]])
    treeS.grid(column = 0, row = 0, sticky = (W, N, E, S))

    treeE = ttk.Treeview(frame, height = 7, columns = ('col'), takefocus = 0)
    treeE.heading('#0', text = tr("help.nonhall.streaks.tree.battle.ender"))
    treeE.column('#0', width = width)
    treeE.heading('col', text = heading)
    treeE.column('col', width = width)
    treeE.insert('', 'end', text = core.BattleNum.e1.value, values = [evalues[0]])
    treeE.insert('', 'end', text = core.BattleNum.e2.value, values = [evalues[1]])
    treeE.insert('', 'end', text = core.BattleNum.e3.value, values = [evalues[2]])
    treeE.insert('', 'end', text = core.BattleNum.e4.value, values = [evalues[3]])
    treeE.insert('', 'end', text = core.BattleNum.e5.value, values = [evalues[4]])
    treeE.insert('', 'end', text = core.BattleNum.e6.value, values = [evalues[5]])
    treeE.insert('', 'end', text = core.BattleNum.e7.value, values = [evalues[6]])
    treeE.grid(column = 1, row = 0, sticky = (W, N, E, S))

    return frame

# returns a frame with two treeviews next to each other containg the values for the ranks
def makeRankTrees(parent, width, heading, values):

    frame = ttk.Frame(parent)
    frame.columnconfigure(0, weight = 1)
    frame.columnconfigure(1, weight = 1) 

    tree1 = ttk.Treeview(frame, height = 5, columns = ('col'), takefocus = 0)
    tree1.heading('#0', text = tr("help.hall.rank.tree.rank"))
    tree1.column('#0', width = width)
    tree1.heading('col', text = heading)
    tree1.column('col', width = width)
    tree1.grid(column = 0, row = 0, sticky = (W, N, E, S))

    tree2 = ttk.Treeview(frame, height = 5, columns = ('col'), takefocus = 0)
    tree2.heading('#0', text = tr("help.hall.rank.tree.rank"))
    tree2.column('#0', width = width)
    tree2.heading('col', text = heading)
    tree2.column('col', width = width)
    tree2.grid(column = 1, row = 0, sticky = (W, N, E, S))

    for rank, value in enumerate(values, start = 1):
        tree = tree1 if rank < 6 else tree2
        tree.insert('', 'end', text = rank, values = value)

    return frame

def makeSpendTree(parent, width, height, level_costs, level_values):

    tree = ttk.Treeview(parent, height = height, columns = ('cost'), takefocus = 0)
    tree.heading('#0', text = tr("help.tricks.castle.spending_points.tree.feature"))
    tree.column('#0', width = width)
    tree.heading('cost', text = tr("help.tricks.castle.spending_points.tree.cost"))
    tree.column('cost', width = 25)
    level_ids = []
    level_ids.append(tree.insert('', 'end', text = tr("help.tricks.castle.spending_points.tree.unlock.1"), values = ["---"], open = True))
    for level, cost in enumerate(level_costs, start = 2):
        level_ids.append(tree.insert('', 'end', text = tr(f"help.tricks.castle.spending_points.tree.unlock.{level}"), values = [cost], open = True))
    for level, values in enumerate(level_values):
        for feature, cost in values:
            tree.insert(level_ids[level], 'end', text = tr(f"help.tricks.castle.spending_points.tree.{feature}"), values = [cost])

    return tree
