def add_new_prod(key_prod_pairs, cnf, list_of_keys):
    """ Add the new productions after the removal of epsilon """

    return 0


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
        productions = cnf.get(key, ())
        for production in productions:
            if has_key(production, list_of_keys):
                key_prod_pairs.append((key, production))

    add_new_prod(key_prod_pairs, cnf, list_of_keys)

    return key_prod_pairs


def get_eps_keys(cnf):
    """Find keys that have null productions"""
    list_of_keys = []
    for key in cnf:
        productions = cnf.get(key, ())
        if "" in productions:
            list_of_keys.append(key)

    epsilon_keys_in_prod(list_of_keys, cnf)

    return list_of_keys



def remove_eps_prod(cnf):
    """ Find null productions
        Add new productions for the found state
        Wherever that found symbol occurs on the right-hand side, you remove it
        In case of multiple occurrences on the same productions, each removal is an individual result """
    get_eps_keys(cnf)

    pass


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


CFG = {
    "S": "B",
    "A": ("aX", "bX"),
    "X": ("", "BX", "b"),
    "B": "AXaD",
    "D": ("aD", "a"),
    "C": "Ca",
}

CFG = cfg_to_cnf(CFG)
