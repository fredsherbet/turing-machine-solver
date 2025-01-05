
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

def neighbours(g):
    """Provide all pairs of neighbours (each pair is given in order)"""
    yield (g.b, g.y)
    yield (g.y, g.p)

def count_asc(g):
    asc = sum(1 for a,b in neighbours(g) if b-a == 1)
    if asc == 0:
        return 0
    return asc + 1

card_rules = {
    3: [ # Yellow vs 3
        Rule("g.y <  3"),
        Rule("g.y == 3"),
        Rule("g.y >  3"),
    ],
    7: [ # Purple is odd or even?
        Rule("g.p % 2 == 0"),
        Rule("g.p % 2 == 1"),
    ],
    9: [ # How many 3s?
        Rule("count_digits(g, '== 3') == 0"),
        Rule("count_digits(g, '== 3') == 1"),
        Rule("count_digits(g, '== 3') == 2"),
        #Rule("count_digits(g, '== 3') == 3"),
    ],
    11: [ # Blue vs yellow
        Rule("g.b <  g.y"),
        Rule("g.b == g.y"),
        Rule("g.b >  g.y"),
    ],
    12: [ # Blue vs purple
        Rule("g.b <  g.p"),
        Rule("g.b == g.p"),
        Rule("g.b >  g.p"),
    ],
    14: [ # Which is smallest? 
        Rule("g.b < g.p and g.b < g.y"),
        Rule("g.y < g.b and g.y < g.p"),
        Rule("g.p < g.y and g.p < g.b"),
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
    17: [ # How many digits are even?
        Rule("count_digits(g, '% 2 == 0') == 0"),
        Rule("count_digits(g, '% 2 == 0') == 1"),
        Rule("count_digits(g, '% 2 == 0') == 2"),
        Rule("count_digits(g, '% 2 == 0') == 3"),
    ],
    22: [ # Asc/Desc/no order?
        Rule("g.b > g.y and g.y > g.p"),
        Rule("g.b < g.y and g.y < g.p"),
        Rule("not((g.b > g.y and g.y > g.p) or (g.b < g.y and g.y < g.p))"),
    ],
    24: [ # Asc sequence length
        Rule("count_asc(g) == 3"),
        Rule("count_asc(g) == 2"),
        Rule("count_asc(g) == 0"),
    ],
    27: [ # A colour is < 4
        Rule("g.b < 4"),
        Rule("g.y < 4"),
        Rule("g.p < 4"),
    ],
    38: [ # Sum of 2 is 6
        Rule("g.b + g.y == 6"),
        Rule("g.b + g.p == 6"),
        Rule("g.y + g.p == 6"),
    ],
    40: [ # One colour vs 3
        Rule("g.b <  3"),
        Rule("g.b == 3"),
        Rule("g.b >  3"),
        Rule("g.y <  3"),
        Rule("g.y == 3"),
        Rule("g.y >  3"),
        Rule("g.p <  3"),
        Rule("g.p == 3"),
        Rule("g.p >  3"),
    ],
    46: [ # How many 3s? Or how many 4s?
        Rule("count_digits(g, '== 3') == 0"),
        Rule("count_digits(g, '== 3') == 1"),
        Rule("count_digits(g, '== 3') == 2"),
        Rule("count_digits(g, '== 4') == 0"),
        Rule("count_digits(g, '== 4') == 1"),
        Rule("count_digits(g, '== 4') == 2"),
    ],
    48: [ # Compares 2 colours
        Rule("g.b <  g.y"),
        Rule("g.b == g.y"),
        Rule("g.b >  g.y"),
        Rule("g.b <  g.p"),
        Rule("g.b == g.p"),
        Rule("g.b >  g.p"),
        Rule("g.y <  g.p"),
        Rule("g.y == g.p"),
        Rule("g.y >  g.p"),
    ]
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

def possible_solutions(rule, rules):
    return [g for r,g in rules if rule in r]

cards = [16, 38, 40, 48]

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
