import copy
from pprint import pprint
import itertools


def remove_at_index(production, index):
    """ removes from string the character at index """
    return production[:index] + production[index + 1:]


def generate_productions(production, index_combinations):
    new_productions = []
    for combination in index_combinations:
        new_production = production
        for index in reversed(combination):
            new_production = remove_at_index(new_production, index)

        new_productions.append(new_production)

    return new_production


def add_new_productions(cnf, list_of_combinations):
    """ Adds to the grammar the newly created productions based on index combinations """
    for triplet in list_of_combinations:
        key, production, combinations = triplet
        new_production = generate_productions(production, combinations)
        cnf[key].append(new_production)

    return 0


def generate_list_of_combinations(list_of_positions, cnf):
    """ Creates a list of combinations of positions that will be deleted """
    list_of_combinations = []
    for triplet in list_of_positions:
        key, production, positions = triplet
        for i in range(1, len(positions) + 1):
            comb = list(itertools.combinations(positions, i))
            list_of_combinations.append((key, production, comb))
    # print("list of comb", list_of_combinations)
    add_new_productions(cnf, list_of_combinations)

    return list_of_combinations


def generate_list_of_positions(key_prod_pairs, list_of_keys, cnf):
    """ Creates the list of positions where the null element is encountered """
    list_of_positions = []
    for pair in key_prod_pairs:
        key, production = pair
        for null_key in list_of_keys:
            if null_key in production:
                list_of_positions.append(
                    (key, production, [i for i, letter in enumerate(production) if letter == null_key]))
    generate_list_of_combinations(list_of_positions, cnf)

    return list_of_positions


def has_key(production, list_of_keys):
    """ Returns true if production contains at least a symbol that leads to null production """
    for key in list_of_keys:
        if key in production:
            return True


def epsilon_keys_in_prod(list_of_keys, cnf):
    """ Finds the productions that contain the Symbol that leads to epsilon
       Returning new productions """
    key_prod_pairs = []
    for key in cnf:
        productions = cnf.get(key)
        for production in productions:
            if has_key(production, list_of_keys):
                key_prod_pairs.append((key, production))
    # print("key production pairs", key_prod_pairs)
    generate_list_of_positions(key_prod_pairs, list_of_keys, cnf)

    return key_prod_pairs


def get_eps_keys(cnf):
    """Find keys that have null productions"""
    global list_of_keys
    list_of_keys = []
    for key in cnf:
        productions = cnf.get(key)
        if "" in productions:
            list_of_keys.append(key)

    epsilon_keys_in_prod(list_of_keys, cnf)

    return list_of_keys


def pop_epsilon(productions):
    return productions.remove("")


def remove_problematic_productions(list_of_keys, cnf):
    for key in cnf.copy():
        productions = cnf.get(key)
        for element in list_of_keys:
            for production in productions:
                if element in production:
                    productions.remove(production)

    return cnf


def remove_eps_prod(cnf):
    """ Find null productions
        Add new productions for the found state
        Wherever that found symbol occurs on the right-hand side, you remove it
        In case of multiple occurrences on the same productions, each removal is an individual result """
    get_eps_keys(cnf)

    for key in cnf.copy():
        productions = cnf.get(key)
        if "" in productions:
            """ Delete epsilon from the list of productions """
            pop_epsilon(productions)
        if len(productions) == 0:
            cnf.pop(key)
            remove_problematic_productions(list_of_keys, cnf)

    return cnf


def complete_unit_prod(cnf, unit_prod_list, key_list):
    """ Function that changes the Unit production with it's productions """
    prod_to_add = []
    for unit, unit_key in zip(unit_prod_list, key_list):
        for key in cnf.copy():
            productions = cnf.get(key)
            for production in productions:
                if unit == key:
                    prod_to_add.append([unit_key, production])
    return prod_to_add


def add_prod_to_grammar(cnf, prod_to_add):
    for pair in prod_to_add:
        uni_key, production = pair
        cnf[uni_key].append(production)
    return cnf


def remove_unit_productions(cnf, unit_prod_list, key_list):
    for unit, unit_key in zip(unit_prod_list, key_list):
        for key in cnf.copy():
            productions = cnf.get(key)
            if unit_key == key:
                productions.remove(unit)
    return cnf


def is_unit(cnf):
    for key in cnf.copy():
        productions = cnf.get(key)
        for production in productions:
            if len(production) == 1 and production.isupper():
                return True


def unit_productions(cnf):
    """ Remove Unit productions from the grammar """
    while is_unit(cnf):
        key_list = []  # initialize a list of all keys that contain unit productions
        unit_prod_list = []  # initialize a list that contain only unit productions
        # prod_to_add = [] # initialize a list of productions that
        for key in cnf.copy():
            productions = cnf.get(key)
            for production in productions:
                if len(production) == 1 and production.isupper():
                    key_list.append(key)
                    unit_prod_list.append(production)
        prod_to_add = complete_unit_prod(cnf, unit_prod_list, key_list)
        add_prod_to_grammar(cnf, prod_to_add)
        remove_unit_productions(cnf,  unit_prod_list, key_list)


def remove_unproductive(cnf, productive):
    for key in cnf.copy():
        if key not in productive:
            del cnf[key]
    return cnf


def all_productive(production, productive):
    """ Returns true if production contains only productive symbols"""
    for character in production:
        if character not in productive:
            return False
        else:
            return True

def find_productive (cnf, terminals):
    """ Takes the grammar and the set of terminals which will be repurposed
        into the set of productive symbols. We will go through the grammar
        and scan for productive symbols until there are not any more new additions.
        Then we will remove those who are not found in our productive set of symbols."""
    productive = terminals
    old_productive = set()

    while old_productive != productive:
        new_productive = productive
        for key in cnf:
            productions = cnf.get(key)
            for production in productions:
                if production.islower():
                    productive.add(key)
                elif all_productive(production, productive):
                    productive.add(key)
        old_productive = productive
        productive = new_productive

    remove_unproductive(cnf, productive)


def is_unreachable(production, unreachable_symbols):
    for element in unreachable_symbols:
        if element in production:
            return True


def remove_unreachable(cnf, unreachable_symbols):
    for key in cnf.copy():
        productions = cnf.get(key)
        for production in productions:
            if is_unreachable(production, unreachable_symbols):
                productions.remove(production)
        if key in unreachable_symbols:
            del cnf[key]


def unreachable(cnf):
    """ Remove unreachable symbols"""
    all_keys = set()
    prod_symbols = set()
    for key in cnf:
        all_keys.add(key)
        productions = cnf.get(key)
        for production in productions:
            for character in production:
                if character.isupper():
                    prod_symbols.add(character)

    unreachable_symbols = all_keys.symmetric_difference(prod_symbols)
    remove_unreachable(cnf,unreachable_symbols)

def is_mixed(production):
    """
    Returns True if a production contains
    term and non-term symbols
    """
    all_lower = production.islower()
    all_upper = production.isupper()

    if all_upper or all_lower:
        return False
    else:
        return True


def substitute_terminals(production):
    """
    Substitute all terminals in production,
    add keys accordingly
    """
    for character in production:
        if character is 'a':
            new_production = production.replace(character, 'Z')
        elif character is 'b':
            new_production = production.replace(character, 'Y')

    return new_production


def remove_mixed(productions):
    """Creates a new list of productions, cleansed of mixed results"""
    mixed_productions = copy.deepcopy(productions)
    for production in mixed_productions:
        production_index = productions.index(production)
        if is_mixed(production):
            productions.pop(production_index)
    return productions


def shorten_production(cnf, key, production, KEYS):
    """ Shorten all productions bigger than 2 characters """
    productions = cnf[key]
    production_index = productions.index(production)

    new_key = KEYS.pop()
    cnf[key][production_index] = production[0] + new_key
    new_production = production[1:]
    cnf[new_key] = [new_production, ]

    if len(new_production) > 2:
        shorten_production(cnf, new_key, new_production, KEYS)


def chomsky_transformation(cnf):
    # Step 0: we add the terminal equivalent transitions (hardcoded)
    cnf['Z'] = ['a']
    cnf['Y'] = ['b']
    # Step 1: All terms in non-terms (for mixed)
    new_cnf = copy.deepcopy(cnf)
    for key in cnf:
        productions = new_cnf.get(key)
        for production in productions:
            if is_mixed(production):
                new_production = substitute_terminals(production)
                productions.append(new_production)
        new_productions = remove_mixed(productions)
        cnf[key] = new_productions

    # Step 2: Bring productions to len 2 (for len >2)
    KEYS = ['W', 'E', 'L', 'U', 'V', 'T', 'P', 'Q', 'R', 'M', 'K', 'N', 'O', 'G', 'H', 'F', 'I', 'J']
    new_cnf2 = copy.deepcopy(cnf)
    for key, productions in new_cnf2.items():
        for production in productions:
            if len(production) > 2:
                shorten_production(cnf, key, production, KEYS)
                KEYS.pop()


def cfg_to_cnf(cfg, terminals):
    """ Transforms Context-Free Grammar to Chomsky Normal Form """

    cnf = cfg

    """ 1. Eliminate epsilon productions
        2. Eliminate unit productions
        3. Eliminate unproductive symbols
        4. Eliminate inaccessible symbols 
        5. Chomsky Normal Form """
    remove_eps_prod(cnf)
    unit_productions(cnf)
    find_productive(cnf,terminals)
    unreachable(cnf)
    chomsky_transformation(cnf)
    pprint(cnf)


CFG = {
    "S": ["B",],
    "A": ["aX", "bX",],
    "X": ["", "BX", "b",],
    "B": ["AXaD",],
    "D": ["aD", "a",],
    "C": ["Ca",],
}

terminals = {"a", "b"}

cfg_to_cnf(CFG,terminals)








