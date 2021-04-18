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

    pprint(cnf)
    return 0


def generate_list_of_combinations(list_of_positions, cnf):
    """ Creates a list of combinations of positions that will be deleted """
    list_of_combinations = []
    for triplet in list_of_positions:
        key, production, positions = triplet
        for i in range(1, len(positions) + 1):
            comb = list(itertools.combinations(positions, i))
            list_of_combinations.append((key, production, comb))
    print("list of comb", list_of_combinations)
    add_new_productions(cnf, list_of_combinations)

    return list_of_combinations


def generate_list_of_positions(key_prod_pairs, list_of_keys, cnf):
    """ Creates the list of positions where the null element is encountered """
    list_of_positions = []
    for pair in key_prod_pairs:
        key, production = pair
        for null_key in list_of_keys:
            if null_key in production:
                list_of_positions.append((key, production, [i for i, letter in enumerate(production) if letter == null_key]))
    generate_list_of_combinations(list_of_positions, cnf)
    # print("list of pos", list_of_positions)
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

    # print(list_of_keys)
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

    pprint(cnf)

    return cnf


def cfg_to_cnf(cfg):
    """ Transforms Context-Free Grammar to Chomsky Normal Form """

    cnf = cfg
    # initialize queue

    """ 1. Eliminate epsilon productions
        2. Eliminate unit productions
        3. Eliminate unproductive symbols
        4. Eliminate inaccessible symbols """
    remove_eps_prod(cnf)

    pass


# CFG = {
#     "S": ["B",],
#     "A": ["aX", "bX",],
#     "X": ["", "BX", "b",],
#     "B": ["AXaD",],
#     "D": ["aD", "a",],
#     "C": ["Ca",],
# }

CFG = {
    "S": ["bA", "AC",],
    "A": ["bS", "BC", "AbAa",],
    "B": ["BbaA", "a", "bSa",],
    "C": ["",],
    "D": ["AB",]
}

# pprint(CFG)
#CFG = cfg_to_cnf(CFG)
# get_eps_keys(CFG)
remove_eps_prod(CFG)