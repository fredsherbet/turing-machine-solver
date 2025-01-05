
# Load up the rules
# For each combination of possible rules, determine whether there's one and only one answer
# And also are there any rules that are obsolete? How to spot? Combinations that produce no numbers seem sus; can we analyse those?


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
    for b,y,p in product(range(6), range(6), range(6)):
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
        return eval(self.test_description)(g)


card_rules = {
    3: [ # Yellow vs 3
        Rule("lambda g: g.y < 3"),
        Rule("lambda g: g.y == 3"),
        Rule("lambda g: g.y > 3"),
    ],
    7: [ # Purple is odd or even?
        Rule("lambda g: g.p % 2 == 0"),
        Rule("lambda g: g.p % 2 == 1"),
    ],
    9: [ # How many 3s?
        Rule("lambda g: sum(1 for d in g if d == 3) == 0"),
        Rule("lambda g: sum(1 for d in g if d == 3) == 1"),
        Rule("lambda g: sum(1 for d in g if d == 3) == 2"),
        Rule("lambda g: sum(1 for d in g if d == 3) == 3"),
    ],
    11: [ # Blue vs yellow
        Rule("lambda g: g.b < g.y"),
        Rule("lambda g: g.b == g.y"),
        Rule("lambda g: g.b > g.y"),
    ],
    15: [ # Which is biggest?
        Rule("lambda g: g.b > g.p and g.b > g.y"),
        Rule("lambda g: g.y > g.b and g.y > g.p"),
        Rule("lambda g: g.p > g.y and g.p > g.b"),
    ],
    16: [ # More even or odd digits?
        Rule("lambda g: sum(1 for d in g if d % 2 == 0) >= 2"),
        Rule("lambda g: sum(1 for d in g if d % 2 == 1) >= 2"),
    ],
}

cards = [3, 7, 9, 11, 15, 16]

good_rules = []

for rule_set in product(*(card_rules[c] for c in cards)):
    would_be_valid = [g for g in all_possible_guesses() if all(r.test(g) for r in rule_set)]
    if len(would_be_valid) == 1:
        good_rules.append((rule_set, would_be_valid[0]))
            
print("\n".join(str(r) for r in good_rules))