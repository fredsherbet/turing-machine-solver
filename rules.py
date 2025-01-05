
class Rule:
    def __init__(self, test, description=None):
        self.test_s = test
        self.description = description if description else test

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self)

    def test(self, g):
        #print(f"Rule.test({str(self)}, {g})")
        return eval("lambda g: " + self.test_s)(g)

card_rules = {
    1: [
        Rule("g.b == 1"),
        Rule("g.b >  1"),
    ],
    2: [
        Rule("g.b <  3"),
        Rule("g.b == 3"),
        Rule("g.b >  3"),
    ],
    3: [ # Yellow vs 3
        Rule("g.y < 3", "y < 3"),
        Rule("g.y == 3", "y = 3"),
        Rule("g.y > 3", "y > 3"),
    ],
    4: [
        Rule("g.y < 4", "y < 4"),
        Rule("g.y == 4", "y = 4"),
        Rule("g.y > 4", "y > 4"),
    ],

    5: [ # Blue is odd or even?
        Rule("g.b % 2 == 0", "b is even"),
        Rule("g.b % 2 == 1", "b is  odd"),
    ],
    6: [ # Yellow is odd or even?
        Rule("g.y % 2 == 0", "y is even"),
        Rule("g.y % 2 == 1", "y is  odd"),
    ],
    7: [ # Purple is odd or even?
        Rule("g.p % 2 == 0", "p is even"),
        Rule("g.p % 2 == 1", "p is  odd"),
    ],

    8: [ # How many 1s?
        Rule("count_digits(g, '== 1') == 0", "0 of 1"),
        Rule("count_digits(g, '== 1') == 1", "1 of 1"),
        Rule("count_digits(g, '== 1') == 2", "2 of 1"),
        #Rule("count_digits(g, '== 1') == 3", "3 of 1"),
    ],
    9: [ # How many 3s?
        Rule("count_digits(g, '== 3') == 0", "0 of 3"),
        Rule("count_digits(g, '== 3') == 1", "1 of 3"),
        Rule("count_digits(g, '== 3') == 2", "2 of 3"),
        #Rule("count_digits(g, '== 3') == 3", "3 of 3"),
    ],
    10: [ # How many 4s?
        Rule("count_digits(g, '== 4') == 0", "0 of 4"),
        Rule("count_digits(g, '== 4') == 1", "1 of 4"),
        Rule("count_digits(g, '== 4') == 2", "2 of 4"),
        #Rule("count_digits(g, '== 4') == 3", "3 of 4"),
    ],

    11: [ # Blue vs yellow
        Rule("g.b <  g.y", "b < y"),
        Rule("g.b == g.y", "b = y"),
        Rule("g.b >  g.y", "b > y"),
    ],
    12: [ # Blue vs purple
        Rule("g.b <  g.p", "b < p"),
        Rule("g.b == g.p", "b = p"),
        Rule("g.b >  g.p", "b > p"),
    ],
    13: [ # Yellow vs purple
        Rule("g.y <  g.p", "y < p"),
        Rule("g.y == g.p", "y = p"),
        Rule("g.y >  g.p", "y > p"),
    ],

    14: [ # Which is smallest?
        Rule("g.b < g.p and g.b < g.y", "b is smallest"),
        Rule("g.y < g.b and g.y < g.p", "y is smallest"),
        Rule("g.p < g.y and g.p < g.b", "p is smallest"),
    ],
    15: [ # Which is biggest?
        Rule("g.b > g.p and g.b > g.y", "b is biggest"),
        Rule("g.y > g.b and g.y > g.p", "y is biggest"),
        Rule("g.p > g.y and g.p > g.b", "p is biggest"),
    ],

    16: [ # More even or odd digits?
        Rule("count_digits(g, '% 2 == 0') > 1", "More even digits"),
        Rule("count_digits(g, '% 2 == 1') > 1", "More  odd digits"),
    ],
    17: [ # How many digits are even?
        Rule("count_digits(g, '% 2 == 0') == 0", "0 even digits"),
        Rule("count_digits(g, '% 2 == 0') == 1", "1 even digit "),
        Rule("count_digits(g, '% 2 == 0') == 2", "2 even digits"),
        Rule("count_digits(g, '% 2 == 0') == 3", "3 even digits"),
    ],
    18: [
        Rule("sum(g) % 2 == 0", "Sum of digits is even"),
        Rule("sum(g) % 2 == 1", "Sum of digits is  odd"),
    ],

    19: [
        Rule("g.b + g.y <  6"),
        Rule("g.b + g.y == 6"),
        Rule("g.b + g.y >  6"),
    ],

    20: [ # How many repeating digits?
        Rule("repeating_digits(g) == 3", "A triple number"),
        Rule("repeating_digits(g) == 2", "A number appears twice"),
        Rule("repeating_digits(g) == 0", "No numbers appear multiple times"),
    ],
    21: [ # Any pairs?
        Rule("repeating_digits(g) != 2", "No pairs"),
        Rule("repeating_digits(g) == 2", "A number appears exactly twice"),
    ],

    22: [ # Asc/Desc/no order?
        Rule("g.b > g.y and g.y > g.p", "b > y > p"),
        Rule("g.b < g.y and g.y < g.p", "b < y < p"),
        Rule("not((g.b > g.y and g.y > g.p) or (g.b < g.y and g.y < g.p))", "Not in order"),
    ],

    23: [ # Sum vs 6
        Rule("sum(g) <  6", "Sum of digits < 6"),
        Rule("sum(g) == 6", "Sum of digits = 6"),
        Rule("sum(g) >  6", "Sum of digits > 6"),
    ],

    24: [ # Asc sequence length
        Rule("count_asc(g) == 3", "3 consecutive digits"),
        Rule("count_asc(g) == 2", "2 consecutive digits"),
        Rule("count_asc(g) == 0", "0 consecutive digits"),
    ],
    25: [ # How many asc or desc?
        Rule("count_asc(g) == 0 and count_desc(g) == 0", "no consecutive (asc or desc)"),
        Rule("count_asc(g) == 2 or count_desc(g) == 2", "2 consecutive (asc or desc)"),
        Rule("count_asc(g) == 3 or count_desc(g) == 3", "3 consecutive (asc or desc)"),
    ],


    27: [ # A colour is < 3
        Rule("g.b < 3", "b < 3"),
        Rule("g.y < 3", "y < 3"),
        Rule("g.p < 3", "p < 3"),
    ],
    27: [ # A colour is < 4
        Rule("g.b < 4", "b < 4"),
        Rule("g.y < 4", "y < 4"),
        Rule("g.p < 4", "p < 4"),
    ],
    28: [ # A colour is = 1
        Rule("g.b == 1", "b = 1"),
        Rule("g.y == 1", "y = 1"),
        Rule("g.p == 1", "p = 1"),
    ],
    29: [ # A colour is = 3
        Rule("g.b == 3", "b = 3"),
        Rule("g.y == 3", "y = 3"),
        Rule("g.p == 3", "p = 3"),
    ],
    30: [ # A colour is = 4
        Rule("g.b == 4", "b = 4"),
        Rule("g.y == 4", "y = 4"),
        Rule("g.p == 4", "p = 4"),
    ],
    31: [ # A colour is > 1
        Rule("g.b > 1", "b > 1"),
        Rule("g.y > 1", "y > 1"),
        Rule("g.p > 1", "p > 1"),
    ],
    32: [ # A colour is > 3
        Rule("g.b > 3", "b > 3"),
        Rule("g.y > 3", "y > 3"),
        Rule("g.p > 3", "p > 3"),
    ],

    33: [
        Rule("g.b % 2 == 0", "b is even"),
        Rule("g.b % 2 == 1", "b is  odd"),
        Rule("g.y % 2 == 0", "y is even"),
        Rule("g.y % 2 == 1", "y is  odd"),
        Rule("g.p % 2 == 0", "p is even"),
        Rule("g.p % 2 == 1", "p is  odd"),
    ],

    34: [ # Smallest (or equal smallest)
        Rule("g.b <= g.p and g.b <= g.y", "b is (equal) smallest"),
        Rule("g.y <= g.b and g.y <= g.p", "y is (equal) smallest"),
        Rule("g.p <= g.y and g.p <= g.p", "p is (equal) smallest"),
    ],
    35: [ # Biggest (or equal biggest)
        Rule("g.b >= g.p and g.b >= g.y", "b is (equal) biggest"),
        Rule("g.y >= g.b and g.y >= g.p", "y is (equal) biggest"),
        Rule("g.p >= g.y and g.p >= g.p", "p is (equal) biggest"),
    ],

    36: [
        Rule("sum(g) % 3 == 0", "Sum of digits is a multiple of 3"),
        Rule("sum(g) % 4 == 0", "Sum of digits is a multiple of 4"),
        Rule("sum(g) % 5 == 0", "Sum of digits is a multiple of 5"),
    ],

    37: [ # Sum of 2 is 4
        Rule("g.b + g.y == 4", "b+y = 4"),
        Rule("g.b + g.p == 4", "b+p = 4"),
        Rule("g.y + g.p == 4", "y+p = 4"),
    ],
    38: [ # Sum of 2 is 6
        Rule("g.b + g.y == 6", "b+y = 6"),
        Rule("g.b + g.p == 6", "b+p = 6"),
        Rule("g.y + g.p == 6", "y+p = 6"),
    ],

    39: [ # One colour vs 1
        Rule("g.b == 1"),
        Rule("g.b >  1"),
        Rule("g.y == 1"),
        Rule("g.y >  1"),
        Rule("g.p == 1"),
        Rule("g.p >  1"),
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
    41: [ # One colour vs 4
        Rule("g.b <  4"),
        Rule("g.b == 4"),
        Rule("g.b >  4"),
        Rule("g.y <  4"),
        Rule("g.y == 4"),
        Rule("g.y >  4"),
        Rule("g.p <  4"),
        Rule("g.p == 4"),
        Rule("g.p >  4"),
    ],

    42: [ # One colour is smallest, or largest
        Rule("g.b < g.p and g.b < g.y", "b is smallest"),
        Rule("g.y < g.b and g.y < g.p", "y is smallest"),
        Rule("g.p < g.y and g.p < g.b", "p is smallest"),
        Rule("g.b > g.p and g.b > g.y", "b is biggest"),
        Rule("g.y > g.b and g.y > g.p", "y is biggest"),
        Rule("g.p > g.y and g.p > g.b", "p is biggest"),
    ],

    43: [ # Blue vs another colour
        Rule("g.b <  g.y"),
        Rule("g.b <  g.p"),
        Rule("g.b == g.y"),
        Rule("g.b == g.p"),
        Rule("g.b >  g.y"),
        Rule("g.b >  g.p"),
    ],
    44: [ # Yellow vs another colour
        Rule("g.y <  g.b"),
        Rule("g.y <  g.p"),
        Rule("g.y == g.b"),
        Rule("g.y == g.p"),
        Rule("g.y >  g.b"),
        Rule("g.y >  g.p"),
    ],


    45: [ # How many 1s? Or how many 3s?
        Rule("count_digits(g, '== 3') == 0", "0 of 3"),
        Rule("count_digits(g, '== 3') == 1", "1 of 3"),
        Rule("count_digits(g, '== 3') == 2", "2 of 3"),
        Rule("count_digits(g, '== 1') == 0", "0 of 1"),
        Rule("count_digits(g, '== 1') == 1", "1 of 1"),
        Rule("count_digits(g, '== 1') == 2", "2 of 1"),
    ],
    46: [ # How many 3s? Or how many 4s?
        Rule("count_digits(g, '== 3') == 0", "0 of 3"),
        Rule("count_digits(g, '== 3') == 1", "1 of 3"),
        Rule("count_digits(g, '== 3') == 2", "2 of 3"),
        Rule("count_digits(g, '== 4') == 0", "0 of 4"),
        Rule("count_digits(g, '== 4') == 1", "1 of 4"),
        Rule("count_digits(g, '== 4') == 2", "2 of 4"),
    ],
    46: [ # How many 1s? Or how many 4s?
        Rule("count_digits(g, '== 1') == 0", "0 of 1"),
        Rule("count_digits(g, '== 1') == 1", "1 of 1"),
        Rule("count_digits(g, '== 1') == 2", "2 of 1"),
        Rule("count_digits(g, '== 4') == 0", "0 of 4"),
        Rule("count_digits(g, '== 4') == 1", "1 of 4"),
        Rule("count_digits(g, '== 4') == 2", "2 of 4"),
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

def repeating_digits(g):
    max_repeat = max(g.count(d) for d in g)
    return max_repeat if max_repeat > 1 else 0
