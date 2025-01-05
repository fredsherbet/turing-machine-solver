from itertools import product, combinations
import argparse
import sys
from rules import card_rules

def solve_for_cards(cards):
    """Analyse the cards, and figure out what possible rules and answers there are"""
    # Turing Machine relies on the following facts:
    #   * There is only one solution (i.e. the rules must have only a single code that fits)
    #   * Every card is needed to determine the solution (i.e. no card is redundant)
    #
    # We'll use the first fact to get a list of candidates, then filter it down by eliminating
    # candidates that have redundant cards.

    # Do we know all the rules needed?
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
    options = Options(cards)
    #options.short_print_rules()

    # Can we eliminate some, due to some rules being redundant?
    options.eliminate_redundant_cards()
    print(f"\nIgnoring rules that contain redundant rules (got {len(options)}):")
    options.short_print_rules()

    if len(options) > 1:
        # We don't have a single solution. Can we help the player decide what to do?
        print("\nThat means:\n")
        options.print_card_information()


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


class Option:
    def __init__(self, solution, rules):
        self.solution = solution
        self.rules = rules

    def has_redundant_card(self):
        for r in combinations(self.rules, len(self.rules)-1):
            if find_unique_solution(r):
                # Found a unique solution, despite ignoring a rule
                #print(f"{g}: {rule_set} IS BAD because subset {r} gives a unique solution")
                return True
        return False

class Options:
    def __init__(self, cards):
        self.cards = cards
        self.options = list(self._find_rules_that_produce_single_result())
        
    def __len__(self):
        return len(self.options)

    def eliminate_redundant_cards(self):
        self.options = [o for o in self.options if not o.has_redundant_card()]

    def short_print_rules(self):
        print("\n".join(f"{o.solution}: {o.rules}" for o in self.options))

    def print_card_information(self):
        for card in self.cards:
            for rule in card_rules[card]:
                if all(rule in o.rules for o in self.options):
                    print(f"* Card {card} is definitely `{rule}`")
                    break
            else:
                print(f"* Card {card} could be {"".join(
                    f"\n    * `{rule}` ({", ".join(str(s) for s in self._possible_solutions_for_rule(rule))})" 
                    for rule in card_rules[card] if any(rule in o.rules for o in self.options))
                }")

    def _find_rules_that_produce_single_result(self):
        for rule_set in product(*(card_rules[c] for c in self.cards)):
            g = find_unique_solution(rule_set)
            if g:
                yield Option(g, rule_set)
    
    def _possible_solutions_for_rule(self, rule):
        return (o.solution for o in self.options if rule in o.rules)

def find_unique_solution(rule_set):
    count = 0
    for g in Guess.all_possible_guesses():
        if all(r.test(g) for r in rule_set):
            good_guess = g
            count += 1
            if count > 1:
                break
    if count == 1:
        return good_guess

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
