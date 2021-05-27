import re


def parse(word_to_verify, start_symbol, parsing_table):
    """ Parsing the given string and checking
        if the given string is either or not
        accepted by the given grammar rules """
    # flag variable in order to print if the input is successful or not
    flag = 0
    # adding end of string character ($)
    word_to_verify = word_to_verify + "$"
    # stack initialization
    stack = []
    # adding the end of string character to the stack ($)
    stack.append("$")
    stack.append(start_symbol)

    character_index = 0

    while len(stack) > 0:
        top = stack[len(stack) - 1]
        print("Top =>", top)
        current_input = word_to_verify[character_index]
        print("Current_Input => ", current_input)
        if top == current_input:
            stack.pop()
            character_index = character_index + 1
        else:
            key = top, current_input
            print(key)

            if key not in parsing_table:
                flag = 1
                break

            production = parsing_table[key]
            if production != '@':
                production = production[::-1]
                production = list(production)

                stack.pop()

                for element in production:
                    stack.append(element)
            else:
                stack.pop()

    if flag == 0:
        print("String accepted!")
    else:
        print("String not accepted!")


def ll1_parsing_table(follow, productions):
    print("\nParsing Table\n")

    table = {}
    for key in productions:
        for production in productions[key]:
            if production != '@':
                for element in first(production, productions):
                    table[key, element] = production
            else:
                for element in follow[key]:
                    table[key, element] = production

    for key, val in table.items():
        print(key, "=>", val)
    print("\n")

    return table


def follow(left_hand_side, productions, follow_dict):
    """ 1) FOLLOW(S) = { $ }   // where S is the starting Non-Terminal
        2) If A -> pBq is a production, where p, B and q are any grammar symbols,
        then everything in FIRST(q)  except Є is in FOLLOW(B).
        3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
        4) If A->pBq is a production and FIRST(q) contains Є,
        then FOLLOW(B) contains { FIRST(q) – Є } U FOLLOW(A) """
    if len(left_hand_side) != 1:
        return {}

    for key in productions:
        for production in productions[key]:
            character_occurrence = production.find(left_hand_side)
            if character_occurrence != -1:
                if character_occurrence == (len(production) - 1):
                    if key != left_hand_side:
                        if key in follow_dict:
                            temp = follow_dict[key]
                        else:
                            follow_dict = follow(key, productions, follow_dict)
                            temp = follow_dict[key]
                        follow_dict[left_hand_side] = follow_dict[left_hand_side].union(temp)
                else:
                    first_of_next_symbol = first(production[character_occurrence + 1:], productions)
                    if '@' in first_of_next_symbol:
                        if key != left_hand_side:
                            if key in follow_dict:
                                temp = follow_dict[key]
                            else:
                                follow_dict = follow(key, productions, follow_dict)
                                temp = follow_dict[key]
                            follow_dict[left_hand_side] = follow_dict[left_hand_side].union(temp)
                            follow_dict[left_hand_side] = follow_dict[left_hand_side].union(first_of_next_symbol) - {'@'}
                    else:
                        follow_dict[left_hand_side] = follow_dict[left_hand_side].union(first_of_next_symbol)
    return follow_dict


def first(left_hand_side, productions):
    """  1. If x is a terminal, then FIRST(x) = { ‘x’ }
         2. If x-> Є, is a production rule, then add Є to FIRST(x).
         3. If X->Y1 Y2 Y3….Yn is a production,
            1. FIRST(X) = FIRST(Y1)
            2. If FIRST(Y1) contains Є then FIRST(X) = { FIRST(Y1) – Є } U { FIRST(Y2) }
            3. If FIRST (Yi) contains Є for all i = 1 to n, then add Є to FIRST(X)."""
    character = left_hand_side[0]
    first_productions = set()
    if character.isupper():
        for symbol in productions[character]:
            if symbol == '@':
                if len(left_hand_side) != 1:
                    first_productions = first_productions.union(first(left_hand_side[1:], productions))
                else:
                    first_productions = first_productions.union('@')
            else:
                added_productions = first(symbol, productions)
                first_productions = first_productions.union(x for x in added_productions)
    else:
        first_productions = first_productions.union(character)
    return first_productions


# initialize a dictionary for productions
productions = dict()
grammar = open("grammar.txt", "r")
# initialize dictionary for the FIRST values
first_dict = dict()
# initialize dictionary for the FOLLOW values
follow_dict = dict()
flag = 1
start = ""
# splitting the right-hand side and left-hand side of the grammar
for line in grammar:
    split_pattern = re.split("( |->|\n|\||)*", line)
    left_hand_side = split_pattern[0]
    right_hand_side = set(split_pattern[1:-1]) - {''}
    if flag:
        flag = 0
        start = left_hand_side
    productions[left_hand_side] = right_hand_side

print('\nFirst\n')
for left_hand_side in productions:
    first_dict[left_hand_side] = first(left_hand_side, productions)
for element in first_dict:
    print(str(element) + " : " + str(first_dict[element]))
print("")

print('\nFollow\n')

for left_hand_side in productions:
    follow_dict[left_hand_side] = set()

follow_dict[start] = follow_dict[start].union('$')

for left_hand_side in productions:
    follow_dict = follow(left_hand_side, productions, follow_dict)

for left_hand_side in productions:
    follow_dict = follow(left_hand_side, productions, follow_dict)

for element in follow_dict:
    print(str(element) + " : " + str(follow_dict[element]))

ll1_table = ll1_parsing_table(follow_dict, productions)
# will not be accepted
parse("abcdeabcccd", start, ll1_table)
# will be accepted
# parse("abcd", start, ll1_table)