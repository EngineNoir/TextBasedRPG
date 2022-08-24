import random
import json


class Character:
    def __init__(
        self,
        # --------------
        name: str,
        char_class: str,
        level: int,
        # --------------
        strength: int,
        dexterity: int,
        willpower: int,
        # --------------
        health: int,
        mana: int,
        # --------------
        gold: int,
        inventory: list,
        armor: dict,
        weapon: dict,
        amulet: str,
        ring: str,
        # --------------
        spellbook: list,
        # --------------
        max_health, 
        max_mana,
        # --------------
        current_xp: int,
        xp_to_level: int,
    ):
        
        self.name = name
        self.char_class = char_class
        self.level = level
        
        self.strength = strength
        self.dexterity = dexterity
        self.willpower = willpower

        self.health = health
        self.mana = mana

        self.gold = gold
        self.inventory = inventory
        self.armor = armor
        self.weapon = weapon
        self.amulet = amulet
        self.ring = ring

        self.spellbook = spellbook

        self.stealth = False
        self.max_health = max_health
        self.max_mana = max_mana
        self.debuffs = {'poison': False}

        self.current_xp = current_xp
        self.xp_to_level = xp_to_level


    def weapon_attack(self):
        # get the right ability and compute total damage potential
        attack_potential =  self.determine_weapon_ability() + self.weapon['damage']
        successes = 0

        # compute your damage output
        for i in range(attack_potential):
            roll = random.randint(1,6)
            if roll >= 4:
                successes += 1

        # crit if outcome >= 4/5*potential
        if successes >= (4/5)*attack_potential:
            successes += self.weapon['damage']
        
        print('You ' + random.choice(self.weapon['moveset']) + ' dealing ' + str(successes) + ' damage.')
        # need to include the target's defences to set up a "you miss" outcome
        return successes

    def determine_weapon_ability(self):
        # function that accesses a Character value based on weapon ability value
        if self.weapon['ability'] == 'strength':
            return self.strength
        elif self.weapon['ability'] == 'dexterity':
            return self.dexterity
        else:
            return self.willpower

    def gain_xp(self, xp):
        self.current_xp += xp
        print("\nYou've gained " + str(xp) + " XP.")


    def increase_ability(self):
        player_choice = None
        ability_chosen = None
        
        while player_choice not in [1, 2, 3]:
            player_choice = int(input('\nChoose which of the three abilities you wish to increase by 1.'
                                        '\n1. Strength\n2. Dexterity\n3. Willpower\nAttribute to improve: '))
        if player_choice == 1:
            self.strength += 1
            ability_chosen = "Strength"
        elif player_choice == 2:
            self.dexterity += 1
            ability_chosen = "Dexterity"
        elif player_choice == 3:
            self.willpower += 1
            ability_chosen = "Willpower"
        
        print("You have increased your " + ability_chosen + " by 1.")


    def level_up(self):
        print('\nYou have ' + str(self.current_xp) + ' XP. Do you wish to spend ' + str(self.xp_to_level) + ' XP to level up?')
        answer_input = None
        while answer_input not in [1, 2]:
            answer_input = int(input('1. Yes\n2. No\nSpend XP and level up?: '))
            if answer_input == 1:
                self.increase_ability()
                self.level += 1
                self.current_xp -= self.xp_to_level
                self.xp_to_level *= 2
                print('\nYou have successfully leveled up and are now level ' + str(self.level) +
                        '. Congratulations!')
            if answer_input == 2:
                break




def make_character(classes, armors, weapons):
    # need to include try commands in case players input str instead of int or vice versa

    # ask for character's name as a string input
    char_name = str(input("\nWhat is your character's name?: "))
    
    # index over the class names in classes list and present the options
    i = 1
    for char_class in classes:
        print(str(i) + ". " + char_class["class_name"] + ' - ' + char_class["description"])
        i += 1
    
    # makes the player choose a class from the given options
    class_choice = None
    while class_choice not in range(0, len(classes)):
        # we add the minus one because choice number 1 is indexed by 0
        class_choice = int(input('\nWhich class do you choose?: ')) - 1

    chosen_class = classes[class_choice]
    #compute starting health and mana
    starting_health = 10 + chosen_class["strength"] + 0.5*chosen_class["dexterity"]
    starting_mana = 5 + chosen_class["willpower"]

    # get some starting equipment
    starting_weapon = weapons[chosen_class["starter_weapon"]]
    starting_armor = armors[chosen_class["starter_armor"]]

    player_character = Character(char_name, chosen_class["class_name"], 1, chosen_class["strength"], chosen_class["dexterity"],
                        chosen_class["willpower"], starting_health, starting_mana, chosen_class["starter_gold"], [], starting_armor, 
                        starting_weapon, None, None, [], starting_health, starting_mana, 0, 100)

    # save character as json
    save_character(player_character)
    return player_character
    

def load_character():
    # ask for the character name
    char_name = input("\nWhat is your character's name?: ")
    char_sheet = json.load(open(f'characters/{char_name}.json'))
    
    # generate a Character class object with the values from the json file
    player_character = Character(char_sheet['name'], char_sheet['char_class'], char_sheet["level"], char_sheet['strength'], 
                        char_sheet['dexterity'], char_sheet['willpower'], char_sheet['health'], char_sheet['mana'], char_sheet['gold'], 
                        char_sheet['inventory'], char_sheet['armor'], char_sheet['weapon'], char_sheet['amulet'], char_sheet['ring'], 
                        char_sheet['spellbook'], char_sheet['max_health'], char_sheet['max_mana'], char_sheet['current_xp'],
                        char_sheet['xp_to_level'])

    return player_character


def save_character(player_character):
    # create a dictionary from values in player_character (character class object)
    char_dictionary = {'name': player_character.name, 'char_class': player_character.char_class, 'level': player_character.level, 
                        'strength': player_character.strength, 'dexterity': player_character.dexterity, 
                        'willpower': player_character.willpower, 'health': player_character.health, 'mana': player_character.mana, 
                        'gold': player_character.gold, 'inventory': player_character.inventory, 
                        'armor': player_character.armor, 'weapon': player_character.weapon, 'amulet': player_character.amulet,
                        'ring': player_character.ring, 'spellbook': player_character.spellbook, 'stealth': False, 
                        'max_health': player_character.max_health, 'max_mana': player_character.max_mana, 'debuffs': {'poison': False},
                        'current_xp': player_character.current_xp, 'xp_to_level': player_character.xp_to_level}

    # save the dictionary as a json file
    char_sheet_save = json.dumps(char_dictionary, indent=1)
    # export character sheet to the characters directory
    with open(f'characters/{char_dictionary["name"]}' + '.json', 'w') as outfile:
        outfile.write(char_sheet_save)

