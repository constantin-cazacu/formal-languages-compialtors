from pprint import pprint


def union(x, y):
    """ Combines two strings together such that there are no duplicate characters """

    result = list(set(x + y))
    result.sort()
    return "".join(result)


def add_new_state(dfa, state):
    """ Adds new state to dfa, handling productions """

    production = dfa[state[0]]

    for sub_state in state:
        production = tuple(union(x, y)
                           for x, y in zip(production, dfa[sub_state]))

    dfa[state] = production
    return dfa


def extend_dfa(dfa, q_prim, current_state):
    """ Extends dfa and q_prim based on current_state """

    # Check if new states appear
    for state in dfa.get(current_state, ()):

        if not state:
            continue

        if state not in dfa:
            # Add new states in q_prim
            q_prim.append(state)

            # Add new states in dfa
            dfa = add_new_state(dfa, state)

    return dfa, q_prim


def nfa_to_dfa(nfa):
    """ Transforms the given NFA into a DFA """

    # Initialize DFA; Initialize queue;
    dfa = nfa
    q_prim = list(dfa)

    # While new states in queue
    while q_prim:
        current_state = q_prim.pop(0)
        # Extend current state
        # Add new states in queue
        # Add new states/ transitions in DFA
        dfa, q_prim = extend_dfa(dfa, q_prim, current_state)

    return dfa


NFA = {
    "A": ("AB", ""),
    "B": ("C", "B"),
    "C": ("A", "C"),
}


DFA = nfa_to_dfa(NFA)
pprint(DFA)
# pprint(add_new_state(NFA, ""))
# pprint(extend_dfa(NFA, [], "F"))
