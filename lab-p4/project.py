__pokemon__= {}
__effectiveness__ = {}

def __init__():
    """This function loads the data from 'pokemon_stats.csv' and 'type_effectiveness_stats.csv'. This function runs automatically, when the module is imported"""
    import csv
    f = open('pokemon_stats.csv', encoding='utf-8')
    raw_pkmn_data = list(csv.reader(f))
    f.close()
    pkmn_header = raw_pkmn_data[0]
    pkmn_header.pop(0)
    raw_pkmn_data = raw_pkmn_data[1:]
    for pkmn_data in raw_pkmn_data:
        pkmn_data.pop(0)
        pkmn = {}
        for i in range(len(pkmn_header)):
            pkmn[pkmn_header[i]] = pkmn_data[i]
        for stat in pkmn:
            if stat in ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']:
                pkmn[stat] = int(pkmn[stat])
        __pokemon__[pkmn["Name"]] = pkmn

    f = open('type_effectiveness_stats.csv', encoding='utf-8')
    raw_type_data = list(csv.reader(f))
    f.close()
    type_header = raw_type_data[0]
    raw_type_data = raw_type_data[1:]
    for type1 in type_header[1:]:
        __effectiveness__[type1] = {}
    for row in raw_type_data:
        type2 = row[0]
        for i in range(1, len(row)):
            type1 = type_header[i]
            __effectiveness__[type1][type2] = float(row[i])

def print_stats(pkmn):
    """print_stats(pkmn) prints all the statistics of the Pokémon with the name 'pkmn' """
    try:
        for stat in __pokemon__[pkmn]:
            if not (stat == 'Type 2' and __pokemon__[pkmn][stat] == "None"):
                print(stat, ": ", __pokemon__[pkmn][stat])
    except KeyError:
        print(pkmn, " not found in the file")

def get_region(pkmn):
    """get_region(pkmn) returns the region of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Region']

def get_type1(pkmn):
    """get_type1(pkmn) returns Type 1 of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Type 1']

def get_type2(pkmn):
    """get_type2(pkmn) returns Type 2 of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Type 2']

def get_hp(pkmn):
    """get_hp(pkmn) returns the HP of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['HP']

def get_attack(pkmn):
    """get_attack(pkmn) returns the Attack of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Attack']

def get_defense(pkmn):
    """get_defense(pkmn) returns the Defense of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Defense']

def get_sp_atk(pkmn):
    """get_sp_atk(pkmn) returns the Special Attack of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Sp. Atk']

def get_sp_def(pkmn):
    """get_sp_def(pkmn) returns the Special Defense of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Sp. Def']

def get_speed(pkmn):
    """get_speed(pkmn) returns the Speed of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Speed']

def get_type_effectiveness(attacker_type, defender_type):
    """get_type_effectiveness(attacker_type, defender_type) returns the effectiveness of attacker's type against defender's type"""
    return __effectiveness__[attacker_type][defender_type]

__init__()
