# modifying the format of data txt files from how they used to be in the old bfsearch (not v2). start with the old files and do these in order.


# inserts national pokedex numbers into the second position in pokemon.txt
def fixpokemontxt():
    # gets pokemon data
    poke_data = open('pokemon.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(poke_data)):
        poke_data[i] = poke_data[i].split('\t')
        for j in range(len(poke_data[i])):
            poke_data[i][j] = poke_data[i][j].strip()

    # gets dex csv which has names and dex numbers
    dex_data = open('gen4.csv', 'r', encoding="UTF-8").read().splitlines()
    # turns each line into a list
    for i in range(len(dex_data)):
        dex_data[i] = dex_data[i].split(',')

    # create fixed txt
    fixed_poke_data = open('pokemonfixed.txt', 'w')

    # fix and write
    for pset in poke_data:
        for dex in dex_data:
            if pset[1] == dex[1]:
                pset.insert(1, dex[0])
                break
        first = True
        for thing in pset:
            if not first:
                fixed_poke_data.write("\t")
            fixed_poke_data.write(str(thing))
            first = False
        fixed_poke_data.write("\n")


# makes a species data txt from pokemonfixed, to separate species data from set data
def createspeciestxt():
    # gets pokemon data
    fixed_poke_data = open('pokemonfixed.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(fixed_poke_data)):
        fixed_poke_data[i] = fixed_poke_data[i].split('\t')
        for j in range(len(fixed_poke_data[i])):
            fixed_poke_data[i][j] = fixed_poke_data[i][j].strip()

    # sort by dex number
    def sorter(thing):
        return int(thing[1])
    fixed_poke_data.sort(key = sorter)
    
    # create species txt
    species_data = open('species.txt', 'w')

    # create dictionary (to remove duplicates)
    species = {}
    for pset in fixed_poke_data:
        #check for inconsistencies
        #if pset[1] in species:
            #print(pset[1] + " " + pset[2])
            #print(species[pset[1]] == [pset[1], pset[2], pset[-1]])
        
        # add dex, name, base speed to dictionary
        species[pset[1]] = [pset[1], pset[2], pset[-1]]

    #print(species)
    
    for entry in species:
        # dex
        species_data.write(str(species[entry][0]))
        species_data.write("\t")
        # name
        species_data.write(str(species[entry][1]))
        species_data.write("\t")
        # base speed
        species_data.write(str(species[entry][2]))
        
        species_data.write("\n")


# makes a sets data txt from pokemonfixed, to separate species data from set data
def createsetstxt():
    # gets pokemon data
    fixed_poke_data = open('pokemonfixed.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(fixed_poke_data)):
        fixed_poke_data[i] = fixed_poke_data[i].split('\t')
        for j in range(len(fixed_poke_data[i])):
            fixed_poke_data[i][j] = fixed_poke_data[i][j].strip()

    # create sets txt
    sets_data = open('sets.txt', 'w')

    # fix and write
    for pset in fixed_poke_data:
        # remove base speed from sets
        del pset[-1]
        # remove formatted evs from sets (it's unnecessary)
        del pset[-1]
        # remove species name from sets
        del pset[2]
        # remove nickname from sets (it's unnecessary)
        del pset[3]
        
        first = True
        for thing in pset:
            if not first:
                sets_data.write("\t")
            sets_data.write(str(thing))
            first = False
        sets_data.write("\n")
    

# oops! turns out i had the trainer IVs wrong! i was using numbers for the battle factory, not the battle tower.
# this fixes the ivs to use the battle tower numbers.
def fixtrainerivs():
    # gets trainer data
    trainer_data = open('trainers.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(trainer_data)):
        trainer_data[i] = trainer_data[i].split('\t')
        for j in range(len(trainer_data[i])):
            trainer_data[i][j] = trainer_data[i][j].strip()

    # create fixed txt
    fixed_trainer_data = open('trainersfixed.txt', 'w')

    # fix and write
    for tinfo in trainer_data:
        if tinfo[1] == '0':
            tinfo[1] = 3
        elif tinfo[1] == '4':
            tinfo[1] = 6
        elif tinfo[1] == '8':
            tinfo[1] = 9
        elif tinfo[1] == '12':
            tinfo[1] = 12
        elif tinfo[1] == '16':
            tinfo[1] = 15
        elif tinfo[1] == '20':
            tinfo[1] = 18
        elif tinfo[1] == '24':
            tinfo[1] = 21
        elif tinfo[1] == '31':
            tinfo[1] = 31
        else:
            raise ValueError("Weird IV!!! " + str(tinfo[1]))
        
        first = True
        for thing in tinfo:
            if not first:
                fixed_trainer_data.write("\t")
            fixed_trainer_data.write(str(thing))
            first = False
        fixed_trainer_data.write("\n")
          

'''
--https://bulbapedia.bulbagarden.net/wiki/List_of_Battle_Frontier_Trainers_(Generation_IV)--

IV Distribution for Battle Tower, Battle Castle and Battle Arcade.

    Trainers 1 to 100 use Pokémon with 3 IVs
    Trainers 101 to 120 use Pokémon with 6 IVs
    Trainers 121 to 140 use Pokémon with 9 IVs
    Trainers 141 to 160 use Pokémon with 12 IVs
    Trainers 161 to 180 use Pokémon with 15 IVs
    Trainers 181 to 200 use Pokémon with 18 IVs
    Trainers 201 to 220 use Pokémon with 21 IVs
    Trainers 221 to 302 use Pokémon with 31 IVs

IV Distribution for Battle Factory. -NOTE: trainers aren't limited by their normal roster in the battle factory.

    Trainers 1 to 100 use Pokémon with 0 IVs
    Trainers 101 to 120 use Pokémon with 4 IVs
    Trainers 121 to 140 use Pokémon with 8 IVs
    Trainers 141 to 160 use Pokémon with 12 IVs
    Trainers 161 to 180 use Pokémon with 16 IVs
    Trainers 181 to 200 use Pokémon with 20 IVs
    Trainers 201 to 220 use Pokémon with 24 IVs
    Trainers 221 to 302 use Pokémon with 31 IVs

IV Distribution for Battle Hall. -NOTE: battle hall uses a completely different set of pokemon.

    Rank 1 use Pokémon with 8 IVs
    Rank 2 use Pokémon with 10 IVs
    Rank 3 use Pokémon with 12 IVs
    Rank 4 use Pokémon with 14 IVs
    Rank 5 use Pokémon with 16 IVs
    Rank 6 use Pokémon with 18 IVs
    Rank 7 use Pokémon with 20 IVs
    Rank 8 use Pokémon with 22 IVs
    Rank 9 use Pokémon with 24 IVs
    Rank 10 use Pokémon with 26 IVs
'''

# get slightly better trainer info from bulbapedia's table.
# this includes trainer gender, snow ace trainers, and the "end of streak battle" indicator (note that this includes battles 21 and 49 - which aren't actually used since those are palmer's battles).
# make sure to manually add palmer to the end!
def bettertrainerdatafromhtml():
    import os
    from enum import Enum
    from html.parser import HTMLParser

    class Battle(Enum):
        m1 = "1 - 7"
        m2 = "8 - 14"
        m3 = "15 - 21"
        m4 = "22 - 28"
        m5 = "29 - 35"
        m6 = "36 - 42"
        m7 = "43 - 49"
        e1 = "7"
        e2 = "14"
        e3 = "21"
        e4 = "28"
        e5 = "35"
        e6 = "42"
        e7 = "49"
        beyond = "50+"

        '''
        def toend(self):
            if self == Battle.m1:
                return Battle.e1
            elif self == Battle.m2:
                return Battle.e2
            elif self == Battle.m3:
                return Battle.e3
            elif self == Battle.m4:
                return Battle.e4
            elif self == Battle.m5:
                return Battle.e5
            elif self == Battle.m6:
                return Battle.e6
            elif self == Battle.m7:
                return Battle.e7
            else:
                return self
        '''

    class State(Enum):
        READING_TRAINER_ID = 0
        READING_TRAINER_CLASS = 1
        READING_TRAINER_NAME = 2
        READING_STREAKS = 3
        DONE_READING_TRAINER = 99
        
    class MyHTMLParser(HTMLParser):

        streak_counter = 0
        hasWrittenStreak = False

        state = State.DONE_READING_TRAINER
        
        def handle_starttag(self, tag, attrs):
            if tag == 'tr' and MyHTMLParser.state == State.DONE_READING_TRAINER:
                MyHTMLParser.state = State.READING_TRAINER_ID
            elif tag == 'a' and MyHTMLParser.state == State.READING_TRAINER_ID:
                MyHTMLParser.state = State.READING_TRAINER_CLASS
            elif tag == 'a' and MyHTMLParser.state == State.READING_TRAINER_CLASS:
                wfile.write("\t")
                MyHTMLParser.state = State.READING_TRAINER_NAME
            elif tag == 'th':
                MyHTMLParser.state = State.READING_STREAKS
                for attr in attrs:
                    if attr[0] == 'colspan':
                        wfile.close()
                        raise Exception("COMPLETE!")
                for attr in attrs:
                    if attr[0] == 'style':
                        if MyHTMLParser.hasWrittenStreak:
                            wfile.write(",")
                        if MyHTMLParser.streak_counter == 7:
                            battle = 14
                        elif attr[1] == 'background:#E7C46E':
                            battle = MyHTMLParser.streak_counter + 7
                        elif attr[1] == 'background:#D6D6D6':
                            battle = MyHTMLParser.streak_counter
                        wfile.write(list(Battle)[battle].value)
                        MyHTMLParser.hasWrittenStreak = True
                        
                MyHTMLParser.streak_counter += 1

        def handle_endtag(self, tag):
            if tag == 'tr' and MyHTMLParser.state == State.READING_STREAKS:
                MyHTMLParser.state = State.DONE_READING_TRAINER
                MyHTMLParser.streak_counter = 0
                MyHTMLParser.hasWrittenStreak = False
                wfile.write("\n")

        def handle_data(self, data):
            if data != '\n':
                if MyHTMLParser.state == State.READING_TRAINER_ID:
                    tid = int(data.strip())
                    wfile.write(str(tid))
                    wfile.write("\t")
                    # ivs
                    if tid >= 1 and tid <= 100:
                        wfile.write("3")
                    elif tid >= 101 and tid <= 120:
                        wfile.write("6")
                    elif tid >= 121 and tid <= 140:
                        wfile.write("9")
                    elif tid >= 141 and tid <= 160:
                        wfile.write("12")
                    elif tid >= 161 and tid <= 180:
                        wfile.write("15")
                    elif tid >= 181 and tid <= 200:
                        wfile.write("18")
                    elif tid >= 201 and tid <= 220:
                        wfile.write("21")
                    elif tid >= 221 and tid <= 302:
                        wfile.write("31")
                    wfile.write("\t")
                elif MyHTMLParser.state == State.READING_TRAINER_CLASS:
                    # gender
                    if '♂' in data or '♀' in data:
                        wfile.write(" ")
                        wfile.write(str(data.strip()))
                    # note for snow ace trainers
                    elif '*' in data:
                        wfile.write(" (Snow)")
                    else:
                        wfile.write(str(data.strip()))
                elif MyHTMLParser.state == State.READING_TRAINER_NAME:
                    wfile.write(data.strip())
                    wfile.write("\t")

        wfile = None

        def setWFile(self, newWfile):
            wfile = newWfile
            
            
    with open("htmltrainers.txt", "w", encoding = "UTF-8") as wfile:
        with open("trainers table (no header) - bulbapedia.html", "r", encoding = "UTF-8") as file:
            
            parser = MyHTMLParser()
            parser.setWFile(wfile)
            
            for line in file:
                parser.feed(line)

# combines htmltrainers.txt with the set data from trainers.txt, and uses species.txt to put set data in nat dex order
def combinedtrainers():
    # gets trainer data
    trainer_data = open('trainers.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(trainer_data)):
        trainer_data[i] = trainer_data[i].split('\t')
        for j in range(len(trainer_data[i])):
            trainer_data[i][j] = trainer_data[i][j].strip()

    # set data as a list of lists in order of trainer id
    set_data = []
    for i in range(len(trainer_data)):
        set_data.append(trainer_data[i][5].split(','))
        set_data[-1] = set_data[-1][:-1]
        #print(set_data[-1])

    # gets species data
    species_data = open('species.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(species_data)):
        species_data[i] = species_data[i].split('\t')
        for j in range(len(species_data[i])):
            species_data[i][j] = species_data[i][j].strip()

    # species data as a list of names with 1-4 for each (a reference order)
    species_possibles = []
    for i in range(len(species_data)):
        for sid in range(1,5):
            species_possibles.append(str(species_data[i][1]) + " " + str(sid))

    #print(species_possibles)
    
    for i in range(len(set_data)):
        set_data[i] = [str for x in species_possibles for str in set_data[i] if str == x] # apparently this is something that you can do to sort a list according to the order of another list
        #print(set_data[i])

    # gets htmltrainer data
    html_trainer_data = open('htmltrainers.txt', 'r', encoding = "UTF-8").read().splitlines()

    assert len(html_trainer_data) == len(set_data)

    # create fixed txt
    combined_trainer_data = open('combinedtrainers.txt', 'w', encoding = "UTF-8")
    
    # fix and write
    for i in range(len(html_trainer_data)):
        string = html_trainer_data[i] + "\t"
        first = True
        for aset in set_data[i]:
            if not first:
                string += ","
            string += str(aset)
            first = False
        combined_trainer_data.write(string + "\n")


# combinedtrainers.txt
# manually removed trainers listed as being battleable on battles 21 and 49, since those are used for palmer.
# ctrl+f : '\t21,' replace with '\t'
# ctrl+f : '\t49,' replace with '\t'

# combinedtrainers.txt
# manually fixed streak ranges to remove final battles, since those are separate. eg: 1 - 7 -> 1 - 6, etc.



# manually added abilities to species.txt -> species with abilities.txt. abilities are after base speed. if two, separated by comma. i used serebii.
# if the pokemon has only one ability, it should be used in the showdown format copypastable.
# if the pokemon has two, it shouldn't be used in the copypastable, but there should be a note saying this pokemon can have ability a or ability b.




# fix old move/item names in sets.txt
# update names to gen 6+. ThunderPunch -> Thunder Punch, Brightpowder -> Bright Powder, etc.
def updatenames():

    def fixmove(move):
        if move == "ThunderPunch":
            return "Thunder Punch"
        elif move == "ThunderShock":
            return "Thunder Shock"
        elif move == "PoisonPowder":
            return "Poison Powder"
        elif move == "GrassWhistle":
            return "Grass Whistle"
        elif move == "SolarBeam":
            return "Solar Beam"
        elif move == "ExtremeSpeed":
            return "Extreme Speed"
        elif move == "DynamicPunch":
            return "Dynamic Punch"
        elif move == "AncientPower":
            return "Ancient Power"
        elif move == "BubbleBeam":
            return "Bubble Beam"
        elif move == "DragonBreath":
            return "Dragon Breath"
        elif move == "DoubleSlap":
            return "Double Slap"
        elif move == "FeatherDance":
            return "Feather Dance"
        elif move == "SmokeScreen":
            return "Smokescreen"
        elif move == "ViceGrip" or move == "Vice Grip":
            return "Vise Grip"
        elif move == "Softboiled":
            return "Soft-Boiled"
        elif move == "Sand-Attack":
            return "Sand Attack"
        else:
            return move

    def fixitem(item):
        if item == "BlackGlasses":
            return "Black Glasses"
        elif item == "DeepSeaScale":
            return "Deep Sea Scale"
        elif item == "DeepSeaTooth":
            return "Deep Sea Tooth"
        elif item == "TwistedSpoon":
            return "Twisted Spoon"
        elif item == "Silverpowder" or item == "SilverPowder":
            return "Silver Powder"
        elif item == "Brightpowder" or item == "BrightPowder":
            return "Bright Powder"
        elif item == "NeverMeltIce":
            return "Never-Melt Ice"
        else:
            return item
            

        
    # gets set data
    set_data = open('sets.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(set_data)):
        set_data[i] = set_data[i].split('\t')
        for j in range(len(set_data[i])):
            set_data[i][j] = set_data[i][j].strip()

    # create fixed txt
    updated_set_data = open('setsupdated.txt', 'w')

    # fix and write
    for sinfo in set_data:
        first = True
        for i in range(len(sinfo)):
            thing = sinfo[i]
            if i == 4:
                thing = fixitem(thing)
            elif i >= 5 and i <= 8:
                thing = fixmove(thing)
            if not first:
                updated_set_data.write("\t")
            updated_set_data.write(str(thing))
            first = False
        updated_set_data.write("\n")
            
 

# make everything a json
# species with abilities, setsupdated, combinedtrainers
# for each file:
# make sure to remove the last comma!
# and then format it in notepad++!
def jsonify():
    #import json


    ### species!
    species_json = open('species.json', 'w', encoding = 'UTF-8')
    
    # gets species data
    species_data = open('species with abilities.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(species_data)):
        species_data[i] = species_data[i].split('\t')
        for j in range(len(species_data[i])):
            species_data[i][j] = species_data[i][j].strip()
            # split abilities
            if j == 3:
                species_data[i][j] = species_data[i][j].split(',')

    # write
    species_json.write('{"species":[\n')
    for species in species_data:
        species_json.write('{"dex":' + species[0] + ',"name":"' + species[1] + '","speed":' + species[2] + ',"abilities":["' + species[3][0] + (('","' + species[3][1]) if len(species[3]) > 1 else '') + '"]},\n')
    species_json.write(']}')

    # make sure to remove the last comma!
    # and then format it in notepad++!
    

    ### sets!
    sets_json = open('sets.json', 'w', encoding = 'UTF-8')

    # changed my mind about using dex number as identifier in sets data. change it back to species name. dex number is used for sorting purposes only.
    def specieslookup(dex):
        for species in species_data:
            if dex == species[0]:
                return species[1]
        raise Exception("Unknown species!?!?!?")
    
    # gets set data
    set_data = open('setsupdated.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(set_data)):
        set_data[i] = set_data[i].split('\t')
        for j in range(len(set_data[i])):
            set_data[i][j] = set_data[i][j].strip()

    # write
    sets_json.write('{"sets":[\n')
    for aset in set_data:
        sets_json.write('{"id":' + aset[0] + ',"species":"' + specieslookup(aset[1]) + '","set":' + aset[2] + ',"nature":"' + aset[3] + '","item":"' + aset[4] + '","moves":["' + aset[5] + '","' + aset[6] + '","' + aset[7] + '","' + aset[8] + '"],"evs":["' + aset[9] + '","' + aset[10] + (('","' + aset[11]) if aset[11] != '' else '') + '"]},\n')
    sets_json.write(']}')

    # make sure to remove the last comma!
    # and then format it in notepad++!

    
    ### trainers!
    trainers_json = open('trainers.json', 'w', encoding = 'UTF-8')
    
    # gets trainer data
    trainer_data = open('combinedtrainers.txt', 'r', encoding = 'UTF-8').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(trainer_data)):
        trainer_data[i] = trainer_data[i].split('\t')
        for j in range(len(trainer_data[i])):
            trainer_data[i][j] = trainer_data[i][j].strip()
            # split streaks and pokemon
            if j == 4 or j == 5:
                trainer_data[i][j] = trainer_data[i][j].split(',')

    # write
    trainers_json.write('{"trainers":[\n')
    for trainer in trainer_data:
        trainers_json.write('{"id":' + trainer[0] + ',"iv":' + trainer[1] + ',"class":"' + trainer[2] + '","name":"' + trainer[3] + '","battles":[')
        first = True
        for streak in trainer[4]:
            if not first:
                trainers_json.write(',')
            trainers_json.write('"' + streak + '"')
            first = False
        trainers_json.write('],"pokemon":')
        '''
        first = True
        for aset in trainer[5]:
            if not first:
                trainers_json.write(',')
            trainers_json.write('"' + aset + '"')
            first = False
        '''
        # instead of ["Vaporeon 1","Vaporeon 2","Vaporeon 3","Vaporeon 4"], do this: {"Vaporeon":[1,2,3,4]}
        tsets = {}
        for aset in trainer[5]:
            thisset = aset.split(' ')
            # Mr. Mime and Mime Jr. mess this up
            if len(thisset) == 3:
                thisset = [thisset[0] + " " + thisset[1], thisset[2]]
            if thisset[0] not in tsets.keys():
                tsets[thisset[0]] = []
            tsets[thisset[0]].append(int(thisset[1]))
        # Farfetch'd messes this up
        trainers_json.write(str(tsets).replace("'", '"').replace('Farfetch"d', "Farfetch'd") + "},\n")
    trainers_json.write(']}')

    # make sure to remove the last comma!
    # and then format it in notepad++!


    


