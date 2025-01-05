
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
    23: [ # Sum vs 6
        Rule("sum(g) <  6"),
        Rule("sum(g) == 6"),
        Rule("sum(g) >  6"),
    ],
    24: [ # Asc sequence length
        Rule("count_asc(g) == 3"),
        Rule("count_asc(g) == 2"),
        Rule("count_asc(g) == 0"),
    ],
    25: [ # How many asc or desc?
        Rule("count_asc(g) == 0 and count_desc(g) == 0"),
        Rule("count_asc(g) == 2 or count_desc(g) == 2"),
        Rule("count_asc(g) == 3 or count_desc(g) == 3"),
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
    44: [ # Yellow vs another colour
        Rule("g.y <  g.b"),
        Rule("g.y <  g.p"),
        Rule("g.y == g.b"),
        Rule("g.y == g.p"),
        Rule("g.y >  g.b"),
        Rule("g.y >  g.p"),
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
