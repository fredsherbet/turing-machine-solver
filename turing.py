
# Load up the rules
# For each combination of possible rules, determine whether there's one and only one answer
# And also are there any rules that are redundant? How to spot? Combinations that produce no numbers seem sus; can we analyse those?


from itertools import *
from collections import *

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

class Rule:
    def __init__(self, test_description):
        self.test_description = test_description

    def __str__(self):
        return self.test_description

    def __repr__(self):
        return str(self)

    def test(self, g):
        #print(f"Rule.test({str(self)}, {g})")
        return eval("lambda g: " + self.test_description)(g)

def count_digits(g, test):
    return sum(1 for d in g if eval("lambda d: d " + test)(d))

card_rules = {
    3: [ # Yellow vs 3
        Rule("g.y < 3"),
        Rule("g.y == 3"),
        Rule("g.y > 3"),
    ],
    7: [ # Purple is odd or even?
        Rule("g.p % 2 == 0"),
        Rule("g.p % 2 == 1"),
    ],
    9: [ # How many 3s?
        Rule("count_digits(g, '== 3') == 0"),
        Rule("count_digits(g, '== 3') == 1"),
        Rule("count_digits(g, '== 3') == 2"),
        Rule("count_digits(g, '== 3') == 3"),
    ],
    11: [ # Blue vs yellow
        Rule("g.b < g.y"),
        Rule("g.b == g.y"),
        Rule("g.b > g.y"),
    ],
    15: [ # Which is biggest?
        Rule("g.b > g.p and g.b > g.y"),
        Rule("g.y > g.b and g.y > g.p"),
        Rule("g.p > g.y and g.p > g.b"),
    ],
    16: [ # More even or odd digits?
        Rule("count_digits(g, '% 2 == 0') > 1"),
        Rule("count_digits(g, '% 2 == 1') > 1"),
    ],
}

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

cards = [3, 7, 9, 11, 15, 16]

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
            bad_rules.add(rule_set)
print(f"\nIgnoring rules that contain redundant rules (Found {len(bad_rules)}):")
good_rules = [(r,g) for r,g in good_rules if r not in bad_rules]
short_print_rules(good_rules)
