from itertools import product, combinations
import argparse
import sys
from rules import card_rules

# Load up the rules
# For each combination of possible rules, determine whether there's one and only one answer
# And also are there any rules that are redundant?

class Guess:
    def __init__(self, b, y, p):
        self.b = b
        self.y = y
        self.p = p

    def __str__(self):
        return f'{self.b}{self.y}{self.p}'

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield self.b
        yield self.y
        yield self.p

class Option:
    def __init__(self, solution, rules):
        self.solution = solution
        self.rules = rules

def all_possible_guesses():
    for b,y,p in product(range(1, 6), range(1, 6), range(1, 6)):
        yield Guess(b, y, p)

def find_unique_solution(rule_set):
    count = 0
    for g in all_possible_guesses():
        if all(r.test(g) for r in rule_set):
            good_guess = g
            count += 1
            if count > 1:
                break
    if count == 1:
        return good_guess

def possible_solutions_for_rule(rule, options):
    return [o.solution for o in options if rule in o.rules]

def short_print_rules(options):
    print("\n".join(f"{o.solution}: {o.rules}" for o in options))

def print_card_information(cards, options):
    for card in cards:
        for rule in card_rules[card]:
            if all(rule in o.rules for o in options):
                print(f"* Card {card} is definitely `{rule}`")
                break
        else:
            print(f"* Card {card} could be \n{"\n".join(
                f"    * `{str(rule)}` ({", ".join(str(s) for s in possible_solutions_for_rule(rule, options))})" 
                for rule in card_rules[card] if any(rule in o.rules for o in options))
            }")

def find_rules_that_produce_single_result(cards):
    for rule_set in product(*(card_rules[c] for c in cards)):
        g = find_unique_solution(rule_set)
        if g:
            yield Option(g, rule_set)

def eliminate_sets_with_redundant_cards(options):
    bad_rules = set()
    for option in options:
        rule_set = option.rules
        for r in combinations(rule_set, len(rule_set)-1):
            if find_unique_solution(r):
                # Found a unique solution, despite ignoring a rule
                #print(f"{g}: {rule_set} IS BAD because subset {r} gives a unique solution")
                bad_rules.add(rule_set)
                break
    return (o for o in options if o.rules not in bad_rules)

def solve_for_cards(cards):

    # Have we got all the rules needed?
    all_good = True
    for c in cards:
        try:
            card_rules[c]
        except KeyError:
            all_good = False
            print(f"I do not know the rules for card {c}")
    if not all_good:
        return
    
    #print("Rule sets that provide a single solution:")
    options = list(find_rules_that_produce_single_result(cards))
    #short_print_rules(options)

    # Can we eliminate some, due to some rules being redundant?
    options = list(eliminate_sets_with_redundant_cards(options))
    print(f"\nIgnoring rules that contain redundant rules (got {len(options)}):")
    short_print_rules(options)

    if len(options) > 1:
        # We don't have a single solution. Can we help the player decide what to do?
        print("\nThat means:\n")
        print_card_information(cards, options)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A Turing Machine game analyser")
    parser.add_argument("-c", "--cards", help="A comma-separated list of the cards in the game", required=True)
    args = parser.parse_args()
    try:
        cards = [int(c) for c in args.cards.split(",")]
    except ValueError:
        print("Cards must be numeric values, separated by commas")
        sys.exit(1)
    solve_for_cards(cards)
