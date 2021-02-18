with open('grammar.txt', 'r') as source_code:
    lines = source_code.readlines()

list_split = [ x.strip().split('->') for x in lines]

grammar_dict = {}
for pair in list_split:
    key = pair[0].strip()
    value = pair[-1].strip()

    if grammar_dict.get(key):
        grammar_dict.get(key).append(value)
    else:
        grammar_dict[key] = [value]

print(grammar_dict)


def check_current(current_state, current_letter):
    return  [x for x in current_state if x[0] == current_letter]


def word_check(grammar, word):
    stack = ["S"]

    while len(stack):
        popped = stack.pop()
        current_char = len(popped) - 1

        if word == popped:
            return True

        if current_char >= len(word):
            continue

        current_letter = word[current_char]
        current_non_terminal = popped[-1]
        current_derived_production = grammar.get(current_non_terminal, [])
        item_to_push = check_current(current_derived_production, current_letter)

        popped = popped[-1]

        item_to_push = [popped + x for x in item_to_push]
        stack.extend(item_to_push)

    return False

assert word_check(grammar_dict, "bb")
assert word_check(grammar_dict, "babcb")
assert word_check(grammar_dict, "bbb")

assert not word_check(grammar_dict, "abb")
assert not word_check(grammar_dict, "ac")
assert not word_check(grammar_dict, "abcababc")