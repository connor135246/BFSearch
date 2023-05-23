# Battle Frontier Search PtHGSS v2 (with pokemon.txt and trainers.txt)
# Grabs pokemon and trainer data from two text docs, organizes it, and allows users to search through it in various ways.


import math


# various search functions that return the indices of the sets that match and warn on invalid entry

def pokemon_search(data, name):
    matches = []

    # convert wrong name to right name
    name = poke_name_fixer(name)
    
    for i in range(len(data)):
        # check species name or nickname
        if name.upper() == data[i][1].upper() or name.upper() == data[i][3].upper():
            matches.append(i)

    if len(matches) < 1:
        print (f"-No Pokemon by the name '{name}'!")
    return matches

# pokemon names with weird characters that may be misspelled in the format [[wrong name, ...], [right name, ...]]
poke_weird_names = [
    ["Farfetchd", "Mr Mime", "Mime Jr", "Porygon 2", "Porygon Z", "PorygonZ"],
    ["Farfetch'd", "Mr. Mime", "Mime Jr.", "Porygon2", "Porygon-Z", "Porygon-Z"]
    ]
assert len(poke_weird_names[0]) == len(poke_weird_names[1])

def poke_name_fixer(poke):
    for i in range(len(poke_weird_names[0])):
        if poke.upper() == poke_weird_names[0][i].upper():
            return poke_weird_names[1][i]
    return poke


def streak_search(data, streak):
    matches = []

    # turn a number into a compatible range 
    streak = streak_fixer(streak)
    if streak == '-1':
        return matches
    
    for i in range(len(data)):
        if streak in data[i][15][3]:
            matches.append(i)

    return matches

def streak_fixer(streak):
    if streak in ('1-6','7','8-13','14','15-20','21','22-27','28','29-34','35','36-41','42','43-48','49','50+'):
        return streak

    try:
        streak = int(streak)
    
        if streak in range(1,7):
            return '1-6'
        elif streak in range(8,14):
            return '8-13'
        elif streak in range(15,21):
            return '15-20'
        elif streak in range(22,28):
            return '22-27'
        elif streak in range(29,35):
            return '29-34'
        elif streak in range(36,42):
            return '36-41'
        elif streak in range(43,49):
            return '43-48'
        elif streak >= 50:
            return '50+'
    except ValueError:
        None
    
    print ("-Invalid battle number!")
    return '-1'


def trainclass_search(data, trainclass):
    matches = []

    # convert wrong name to right name
    trainclass = trainclass_name_fixer(trainclass)
    
    for i in range(len(data)):
        if trainclass.upper() == data[i][15][0].upper():
            matches.append(i)

    if len(matches) < 1:
        print (f"-No Trainer Class has the name '{trainclass}'!")
    return matches

# trainer class names that may be misspelled in the format [[wrong name, ...], [right name, ...]]
trainclass_weird_names = [
    ["Pokemon Ranger", "Pokemon Breeder", "Picnicer", "Poke Fan", "Pokekid"],
    ["PKMN Ranger", "PKMN Breeder", "Picnicker", "Pokefan", "Poke Kid"]
    ]
assert len(trainclass_weird_names[0]) == len(trainclass_weird_names[1])

def trainclass_name_fixer(trainclass):
    # fix the e
    trainclass = trainclass.replace('é', 'e').replace('É', 'E')
    
    for i in range(len(trainclass_weird_names[0])):
        if trainclass.upper() == trainclass_weird_names[0][i].upper():
            return trainclass_weird_names[1][i]
    return trainclass   


def trainname_search(data, trainname):
    matches = []
    for i in range(len(data)):
        if trainname.upper() == data[i][15][1].upper():
            matches.append(i)

    if len(matches) < 1:
        print (f"-No Trainer has the name '{trainname}'!")
    return matches


def item_search(data, item):
    matches = []

    # convert old name to new name
    item = item_name_fixer(item)
    
    for i in range(len(data)):
        if item.upper() == data[i][5].upper():
            matches.append(i)

    if len(matches) < 1:
        print (f"-No item has the name '{item}'!")
    return matches

# items that have different names in gen 4 in the format [[old name, ...], [new name, ...]]
item_name_differences = [
    ["BlackGlasses", "DeepSeaScale", "DeepSeaTooth", "TwistedSpoon", "SilverPowder", "BrightPowder", "NeverMeltIce", ],
    [ "Black Glasses", "Deep Sea Scale", "Deep Sea Tooth", "Twisted Spoon", "Silver Powder", "Bright Powder", "Never-Melt Ice"]
    ]
assert len(item_name_differences[0]) == len(item_name_differences[1])

def item_name_fixer(item):
    for i in range(len(item_name_differences[0])):
        if item.upper() == item_name_differences[0][i].upper():
            return item_name_differences[1][i]
    return item


def move_search(data, move1, move2, move3, move4):
    matches = []
    # sanity check
    if move1 == '' and move2 == '' and move3 == '' and move4 == '':
        return matches

    # convert any old names to new names
    move1 = move_name_fixer(move1)
    move2 = move_name_fixer(move2)
    move3 = move_name_fixer(move3)
    move4 = move_name_fixer(move4)
    
    # start as true if move is ignored. start as false if move is going to be checked for.
    move1found = move1 == ''
    move2found = move2 == ''
    move3found = move3 == ''
    move4found = move4 == ''
    for i in range(len(data)):
        move1accept = False
        move2accept = False
        move3accept = False
        move4accept = False
        for j in range(6,10):
            # if move is ignored, accept the match. if move exists, accept the match and also mark that the move exists.
            if move1 == '':
                move1accept = True
            elif move1.upper() == data[i][j].upper():
                move1accept = True
                move1found = True
            if move2 == '':
                move2accept = True
            elif move2.upper() == data[i][j].upper():
                move2accept = True
                move2found = True
            if move3 == '':
                move3accept = True
            elif move3.upper() == data[i][j].upper():
                move3accept = True
                move3found = True
            if move4 == '':
                move4accept = True
            elif move4.upper() == data[i][j].upper():
                move4accept = True
                move4found = True
        if move1accept and move2accept and move3accept and move4accept:
            matches.append(i)

    # if a given move wasn't ignored and was never found, it will be False. notify of invalid move.
    if not move1found:
        print (f"-No move has the name '{move1}'!")
    if not move2found:
        print (f"-No move has the name '{move2}'!")
    if not move3found:
        print (f"-No move has the name '{move3}'!")
    if not move4found:
        print (f"-No move has the name '{move4}'!")
    return matches

# moves that have different names in gen 4 in the format [[old name, ...], [new name, ...]]
move_name_differences = [
    ["ThunderPunch", "ThunderShock", "PoisonPowder", "GrassWhistle", "SolarBeam", "ExtremeSpeed", "DynamicPunch", "AncientPower", "BubbleBeam", "DragonBreath", "DoubleSlap", "FeatherDance", "SmokeScreen", "ViceGrip", "Vice Grip", "Softboiled", "Sand-Attack"],
    [ "Thunder Punch", "Thunder Shock", "Poison Powder", "Grass Whistle", "Solar Beam", "Extreme Speed", "Dynamic Punch", "Ancient Power", "Bubble Beam", "Dragon Breath", "Double Slap", "Feather Dance", "Smokescreen", "Vise Grip", "Vise Grip", "Soft-Boiled", "Sand Attack"]
    ]
assert len(move_name_differences[0]) == len(move_name_differences[1])

def move_name_fixer(move):
    for i in range(len(move_name_differences[0])):
        if move.upper() == move_name_differences[0][i].upper():
            return move_name_differences[1][i]
    return move


# unused
def print_name_differences_table():
    def formatter(name1, name2):
        print ("{: <20} {: <20}".format(*[name1, name2]))
    
    print ("            - Moves - ")
    formatter("-Name in PtHGSS-", "-Name in Showdown-")
    for i in range(len(move_name_differences[0])):
        formatter(move_name_differences[0][i], move_name_differences[1][i])
    print ("            - Items - ")
    formatter("-Name in PtHGSS-", "-Name in Showdown-")
    for i in range(len(item_name_differences[0])):
        formatter(item_name_differences[0][i], item_name_differences[1][i])


# calculates a set's speed
def speed_calc(merged_set):
    # getting values
    iv = int(merged_set[15][2])
    base = int(merged_set[14])
    if '255 Spe' in merged_set[13]:
        ev = 255
    elif '170 Spe' in merged_set[13]:
        ev = 170
    else:
        ev = 0

    speed = math.floor ( ( (2 * base + iv + math.floor(ev / 4)) * 50 ) / 100 ) + 5

    # nature, if needed
    if merged_set[4] in ('Timid', 'Jolly', 'Hasty', 'Naive'):
        speed = math.floor(speed * 1.1)
    elif merged_set[4] in ('Relaxed', 'Brave', 'Quiet', 'Sassy'):
        speed = math.floor(speed * 0.9)
    
    return speed

# prints out pokemon sets in showdown format for easy copypasting
def showdown_format(merged_set):
    print ("")
    print (merged_set[3] + " w/ " + merged_set[15][2] + " IVs" + " (" + merged_set[1] + ") @ " + merged_set[5] + "  ")
    print ("Level: 50  ")
    print ("EVs: " + merged_set[13] + "  ")
    print (merged_set[4] + " Nature  ")
    print ("IVs: " + merged_set[15][2] + " HP / " + merged_set[15][2] + " Atk / " + merged_set[15][2] + " Def / " + merged_set[15][2] + " SpA / " + merged_set[15][2] + " SpD / " + merged_set[15][2] + " Spe  ")
    print ("- " + merged_set[6] + "  ")
    print ("- " + merged_set[7] + "  ")
    print ("- " + merged_set[8] + "  ")
    print ("- " + merged_set[9] + "  ")
    print ("")
    speed = speed_calc(merged_set)
    print ("Speed (before items/abilities/modifiers): " + str(speed))
    if merged_set[5] == "Choice Scarf":
        speed = math.floor(speed * 1.5)
        print ("Speed (with Choice Scarf): " + str(speed))
    if merged_set[5] == "Iron Ball":
        speed = math.floor(speed * 0.5)
        print ("Speed (with Iron Ball): " + str(speed))
    if merged_set[1] == "Regigigas":
        speed = math.floor(speed * 0.5)
        print ("Speed (during Slow Start): " + str(speed))
    print ("")

# writes pokemon sets in showdown format to file
def write_showdown_format(wfile, poke_set):
    wfile.write("\n")
    wfile.write(poke_set[3] + " (" + poke_set[1] + ") @ " + poke_set[5] + "  \n")
    wfile.write("Level: 50  \n")
    wfile.write("EVs: " + poke_set[13] + "  \n")
    wfile.write(poke_set[4] + " Nature  \n")
    wfile.write("- " + poke_set[6] + "  \n")
    wfile.write("- " + poke_set[7] + "  \n")
    wfile.write("- " + poke_set[8] + "  \n")
    wfile.write("- " + poke_set[9] + "  \n")
    wfile.write("\n")


# returns the set of shared values from a list of lists that can vary in size
# likely copy pasted from some stack overflow answer
def intersectionator(listoflists):
    try:
        return set(listoflists[0]).intersection(intersectionator(listoflists[1:]))
    except IndexError:
        return set(listoflists[0])


# the main way of searching
def input_matching(merged_data, search_set):
    # strip stuff
    for i in range(len(search_set)):
        search_set[i] = search_set[i].strip()
    
    # does all necessary searches
    matches_list = []
    if search_set[0] != '':
        matches_list.append(pokemon_search(merged_data, search_set[0]))
    if search_set[1] != '':
        matches_list.append(streak_search(merged_data, search_set[1]))
    if search_set[2] != '':
        matches_list.append(trainclass_search(merged_data, search_set[2]))
    if search_set[3] != '':
        matches_list.append(trainname_search(merged_data, search_set[3]))
    if search_set[4] != '':
        matches_list.append(item_search(merged_data, search_set[4]))
    if search_set[5] != '' or search_set[6] != '' or search_set[7] != '' or search_set[8] != '':
        matches_list.append(move_search(merged_data, search_set[5], search_set[6], search_set[7], search_set[8]))

    # returns intersections of results
    return list(intersectionator(matches_list))


# the other way of searching
def multi_matching(train_data, merged_data, search_sets):
    # formats search_sets[1] and search_sets[2] and runs them through input_matching (if they were submitted at all)
    matches_lists = [[],[]]  
    if len(search_sets[1]) != 1:
        search_sets[1].insert(1, '')
        search_sets[1].insert(1, '')
        search_sets[1].insert(1, search_sets[0])
        matches_lists[0] = input_matching(merged_data, search_sets[1])
        
        sea1empty = False
        
    else:
        sea1empty = True

    if len(search_sets[2]) != 1:
        search_sets[2].insert(1, '')
        search_sets[2].insert(1, '')
        search_sets[2].insert(1, search_sets[0])
        matches_lists[1] = input_matching(merged_data, search_sets[2])
        
        sea2empty = False
        
    else:
        sea2empty = True

    if sea1empty and sea2empty:
        print ("-No teammates submitted!")
        return []

    # makes a list of all matching pokemon sets for each search set given
    poke_list = [[], []]
    for i in matches_lists[0]:
        if merged_data[i][3] not in poke_list[0]:
            poke_list[0].append(merged_data[i][3])
    for i in matches_lists[1]:
        if merged_data[i][3] not in poke_list[1]:
            poke_list[1].append(merged_data[i][3])

    # makes a list of all possible trainers that could have this combination of pokemon sets
    train_list = []
    for i in range(len(train_data)):
        pok1found = False
        pok2found = False
        for j in range(len(train_data[i][5])):
            if train_data[i][5][j] in poke_list[0]:
                pok1found = True
            if train_data[i][5][j] in poke_list[1]:
                pok2found = True
        # making sure to take care of the possibility that only one pokemon was submitted!
        if (pok1found or sea1empty) and (pok2found or sea2empty):
            train_list.append([train_data[i][2], train_data[i][3]])

    # makes a list of all possible pokemon that match for each possible trainer that matched
    final_list = []
    for i in train_list:
        crossref = input_matching(merged_data, [search_sets[3], search_sets[0], i[0], i[1], '', '', '', '', ''])
        if crossref != []:
            final_list.append(crossref)
    
    return final_list

   
        
# prepares data, then asks for user input
def main():
    print ("  Welcome! This tool lets you search through the possible Pokemon sets in the Platinum/HeartGold/SoulSilver Battle Tower.")
    print ("  The results are in Pokemon Showdown format so you can easily copy-paste them into your favorite damage calculator.")
    print ("  It will also list the possible IV spreads (which depend on the opposing trainer and generally increase with your streak) and calculate the Pokemon's Speed stat.")
    print ("  Protip: Knowing the opposing trainer's class and name can get you much more specific results, so pay attention to it! This is especially effective before battle 50, because those trainers will always have just one possible set per Pokemon.")
    input("-Press enter to build data...")
    
    # gets pokemon data
    poke_data = open('pokemon.txt', 'r').read().splitlines()

    # turns each line into a list and removes excess spaces
    for i in range(len(poke_data)):
        poke_data[i] = poke_data[i].split('\t')
        for j in range(len(poke_data[i])):
            poke_data[i][j] = poke_data[i][j].strip()
            # turns the last few items in each pokemon set into empty lists for later
            if j == 14:
                poke_data[i].append([])
                # deprecated
                '''
                poke_data[i].append([])
                poke_data[i].append([])
                poke_data[i].append([])
                '''
    
    # gets trainer data
    train_data = open('trainers.txt', 'r').read().splitlines()

    # turns each line into a list
    for i in range(len(train_data)):
        train_data[i] = train_data[i].split('\t')
        for j in range(len(train_data[i])):
            # gets rid of those pesky commas at the end of the poke set lists
            if j == 5:
                train_data[i][j] = train_data[i][j][:-1]
            # splits battle set lists and poke set lists
            if j == 4 or j == 5:
                train_data[i][j] = train_data[i][j].split(',')

    # appends trainer data possibilities to the 15 position in each pokemon set in the format [[class, name, iv, [streaks,...]],...]
    for i in range(len(poke_data)):
        for j in range(len(train_data)):
            class_name_iv_streak = [None] * 4
            for k in range(len(train_data[j][5])):
                if poke_data[i][3] == train_data[j][5][k]:
                    class_name_iv_streak[0] = train_data[j][2]
                    class_name_iv_streak[1] = train_data[j][3]
                    class_name_iv_streak[2] = train_data[j][1]
                    class_name_iv_streak[3] = train_data[j][4]
                    poke_data[i][15].append(class_name_iv_streak)

                    # deprecated
                    '''
                    # appends streak/iv possibilities to the 16 position in each pokemon set in the format [streak1, [iv1, ...], ...]
                    for l in range(len(class_name_iv_streak[3])):
                        if class_name_iv_streak[3][l] not in poke_data[i][16]:
                            poke_data[i][16].append(class_name_iv_streak[3][l])
                        slot = poke_data[i][16].index(class_name_iv_streak[3][l])
                        try:
                            if class_name_iv_streak[2] not in poke_data[i][16][slot + 1]:
                                poke_data[i][16][slot + 1].append(class_name_iv_streak[2])
                        except IndexError:
                            poke_data[i][16].append([class_name_iv_streak[2]])
        
                    # keeps track of all possible ivs for each pokemon set at the 17 position
                    if class_name_iv_streak[2] not in poke_data[i][17]:
                        poke_data[i][17].append(class_name_iv_streak[2])
                    # keeps track of all possible streaks for each pokemon set at the 18 position
                    for l in range(len(class_name_iv_streak[3])):
                        if class_name_iv_streak[3][l] not in poke_data[i][18]:
                            poke_data[i][18].append(class_name_iv_streak[3][l])
                    '''

    # expands poke_data into an easier to search format, where every individual pokemon held by every trainer is a separate entry
    merged_data = []
    for i in range(len(poke_data)):
        for j in range(len(poke_data[i][15])):
            this_data = []
            for x in range(15):
                this_data.append(poke_data[i][x])
            this_data.append(poke_data[i][15][j])
            merged_data.append(this_data)
    # each entry is a poke_data line, followed by a [class, name, iv, [streaks,...]]
    #print (merged_data[0])
    #print (merged_data[1000])
    #print (merged_data[-1])
    #print ("total individual pokemon held by all trainers: " + str(len(merged_data))) # over 16000 pokemon! there are, of course, many duplicates.

    print ("-Ready!")
    
    # keep asking questions forever!
    while(True):

        def printinfo(streak):
            print ("-If there's something you don't know, leave it empty.")
            if streak:
                print ("-Enemy trainer possibilities change at battles 1-6, 7, 8-13, 14, 15-20, 21, 22-27, 28, 29-34, 35, 36-41, 42, 43-48, 49, and 50+.")
                print (" -You can use these ranges as input, or just put the exact battle number.")
            print ("-Words/names must match exactly (ignoring case).")
            print (" -For instance, putting 'punch' as a move input won't return any results at all.")
            print ("-Finally, you'll notice that ability and gender aren't listed in the results. They're both random. So if a Pokemon has more than one ability, it could have either one!")

        def rewait():
            input("-Press enter to restart...")
        
        print ("What do you want to do?")
        print ("-Type 1 for general search")
        print ("-Type 2 for Pokemon search based on teammates")
        print ("-Type 3 to create a text file with all 950 Pokemon sets in Pokemon Showdown format")
        #print ("-Type 4 to print all trainers in a dictionary")
        x = input("")

        # general search
        if x == '1':
            print ("-Type out what you know about the opposing pokemon in the following format:")
            print ("Species,Battle Number,Trainer Class,Trainer Name,Item,Move 1,Move 2,Move 3,Move 4")
            printinfo(True)
            print ("Example input 1:staraptor,30,,,,aerial ace,,,")
            print ("Example input 2:staraptor,,bird keeper,sally,,,,,")
            print ("Example input 3:staraptor 4,50+,,,,,,,")
            search_set = input("").split(',')
            if len(search_set) != 9:
                print ("-Invalid entry!")
                rewait()
                continue
            
            final_matches = input_matching(merged_data, search_set)

            print ("---RESULTS---")

            # sends final results to be printed out nicely, and makes sure not to send the same thing twice
            already_sent = []
            for i in final_matches:
                if [merged_data[i][0], merged_data[i][15][2]] not in already_sent:
                    showdown_format(merged_data[i])
                    already_sent.append([merged_data[i][0], merged_data[i][15][2]])
            if len(already_sent) < 1:
                print ("Nothing found!")

        # teammate search
        elif x == '2':
            search_sets = []

            print ("  If you don't recall the name or class of the trainer you're facing, but do know at least one of the other pokemon that the trainer has, then you may be able to figure out the set of the pokemon you're up against.")
            print ("  For example, imagine you're on battle 25. You face a Dragonite. It uses Thunder Wave, and then you defeat it. Then, your opponent sends out a Steelix, and you want to know what moves it has. But you don't recall their trainer class or name.")
            print ("  This method of searching will tell you the Steelix's set!")
            print ("  Yeah, it's a pretty specific scenario...")
            print ("So first, what battle are you on?")
            search_set = streak_fixer(input(""))
            if search_set == '-1':
                rewait()
                continue
            search_sets.append(search_set)

            print ("-Type out what you know about one of the teammates you already battled in the following format:")
            print ("Species,Item,Move 1,Move 2,Move 3,Move 4")
            printinfo(False)
            print ("Example input 1:dragonite,,thunder wave,,,")
            print ("Example input 2:dragonite,lum berry,aerial ace,,,")
            print ("Example input 3:dragonite 1,,,,,")
            search_set = input("").split(',')
            if len(search_set) != 1 and len(search_set) != 6:
                print ("-Invalid entry!")
                rewait()
                continue
            search_sets.append(search_set)
            
            print ("Now do the same for the other teammate you battled, or just press enter if you only know one.")
            search_set = input("").split(',')
            if len(search_set) != 1 and len(search_set) != 6:
                print ("-Invalid entry!")
                rewait()
                continue
            search_sets.append(search_set)
            
            print ("And finally the name of the Pokemon whose set you want to know.")
            search_set = input("")
            if search_set.strip() == '':
                print ("-Empty entry!")
                rewait()
                continue
            search_sets.append(search_set)

            final_list = multi_matching(train_data, merged_data, search_sets)

            print ("---RESULTS---")

            # sends final results to be printed out nicely, and makes sure not to send the same thing twice
            already_sent = []
            for i in final_list:
                for j in i:
                    if [merged_data[j][0], merged_data[j][15][2]] not in already_sent:
                        showdown_format(merged_data[j])
                        already_sent.append([merged_data[j][0], merged_data[j][15][2]])
            if len(already_sent) < 1:
                print ("Nothing found!")

        # create sets text file
        elif x == '3':
            sets_out = open('all sets output.txt', 'w')
            for pset in poke_data:
                write_showdown_format(sets_out, pset)
            sets_out.close()
            print ("Output to 'all sets output.txt'.")

        else:
            print ("-Invalid entry!")

        '''
        # print trainers as a dictionary
        elif x == '4':
            alltrainers = {}
            for trainer in train_data:
                if trainer[2] not in alltrainers:
                    alltrainers[trainer[2]] = []
                alltrainers[trainer[2]].append(trainer[3])
            print(str(alltrainers).replace("],", "]\n   ").replace(":", " ="))

        # count
        elif x == '5':
            uniques = []
            for i in range(len(merged_data)):
                if [merged_data[i][0], merged_data[i][15][2]] not in uniques:
                    uniques.append([merged_data[i][0], merged_data[i][15][2]])
            print("Total individual Pokemon held by all trainers: " + str(len(merged_data))) # 16117
            print("Total 'unique' (a set with a certain iv) Pokemon: " + str(len(uniques))) # 1585

            count_out = open('count_out.json', 'w')
            count_out.write('{\n')
            for i in range(len(merged_data)):
                count_out.write('"' + merged_data[i][15][1] + "'s " + merged_data[i][3] + '": ""')
                if i != len(merged_data) - 1:
                    count_out.write(",\n")
            count_out.write("\n}")
            count_out.close()
        '''

        rewait()        

# run it!
main()
