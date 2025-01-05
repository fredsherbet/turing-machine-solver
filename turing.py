from itertools import product, combinations
import argparse
import sys
from rules import *

# Load up the rules
# For each combination of possible rules, determine whether there's one and only one answer
# And also are there any rules that are redundant? How to spot? Combinations that produce no numbers seem sus; can we analyse those?

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

def all_possible_guesses():
    for b,y,p in product(range(1, 6), range(1, 6), range(1, 6)):
        yield Guess(b, y, p)

def count_digits(g, test):
    return sum(1 for d in g if eval("lambda d: d " + test)(d))

def neighbours(g):
    """Provide all pairs of neighbours (each pair is given in order)"""
    yield (g.b, g.y)
    yield (g.y, g.p)

def count_asc(g):
    asc = sum(1 for a,b in neighbours(g) if b-a == 1)
    return 0 if asc == 0 else asc + 1

def count_desc(g):
    desc = sum(1 for a,b in neighbours(g) if a-b == 1)
    return 0 if desc == 0 else desc + 1

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

def short_print_rules(rules):
    print("\n".join(f"{g}: {r}" for r,g in rules))

def possible_solutions(rule, rules):
    return [g for r,g in rules if rule in r]

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
    
    # Find all rule sets that have a single solution
    print("Rule sets that provide a single solution:")
    good_rules = []
    for rule_set in product(*(card_rules[c] for c in cards)):
        g = find_unique_solution(rule_set)
        if g:
            good_rules.append((rule_set, g))
    short_print_rules(good_rules)

    # Can we eliminate some, due to some rules being redundant?
    bad_rules = set()
    for rule_set, g in good_rules:
        for rules in combinations(rule_set, len(rule_set)-1):
            if find_unique_solution(rules):
                # Found a unique solution, despite ignoring a rule
                #print(f"{g}: {rule_set} IS BAD because {rules} gives a unique solution")
                bad_rules.add(rule_set)
    good_rules = [(r,g) for r,g in good_rules if r not in bad_rules]
    print(f"\nIgnoring rules that contain redundant rules (got {len(good_rules)}):")
    short_print_rules(good_rules)

    if len(good_rules) > 1:
        print("\nThat means:\n")
        # We don't have a single solution. Can we help the player decide what to do?
        for card in cards:
            for rule in card_rules[card]:
                if all(rule in r for r,_ in good_rules):
                    print(f"* Card {card} is definitely `{rule}`")
                    break
            else:
                print(f"* Card {card} could be \n{"\n".join(
                    f"    * `{str(rule)}` ({", ".join(str(s) for s in possible_solutions(rule, good_rules))})" 
                    for rule in card_rules[card] if any(rule in r for r,_ in good_rules))
                }")

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
