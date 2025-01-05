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

    options = Options(cards)

    print(f"\nPossible solutions (got {len(options)}):")
    options.short_print_rules()

    if len(options) > 1:
        # We don't have a single solution. Can we help the player decide what to do?
        print("\nThat means:\n")
        options.print_card_information()

    return options


class Options:
    def __init__(self, cards):
        self.cards = cards
        self.options = [
            o for o in self._find_rules_that_produce_single_result()
            if not o.has_redundant_card()]

    def __len__(self):
        return len(self.options)

    def short_print_rules(self):
        print("\n".join(f"{o.solution}: {o.rules}" for o in self.options))

    def print_card_information(self):
        for card in self.cards:
            rules = self._rules_for_card(card)
            if len(rules) == 1:
                print(f"* Card {card} is definitely {rules[0]}")
            else:
                print(f"* Card {card} could be")
                for r in rules:
                    solutions_s = ", ".join(str(s) for s in self._possible_solutions_for_rule(r))
                    print(f"    * {r} ({solutions_s})")

    def _find_rules_that_produce_single_result(self):
        for rule_set in product(*(card_rules[c] for c in self.cards)):
            o = Option(rule_set)
            if o.has_unique_solution():
                yield o

    def _possible_solutions_for_rule(self, rule):
        return (o.solution for o in self.options if rule in o.rules)

    def _rules_for_card(self, card):
        return [r for r in card_rules[card] if any(r in o.rules for o in self.options)]


class Option:
    def __init__(self, rules):
        self.rules = rules
        self.solution = self.find_unique_solution()

    def has_unique_solution(self):
        return self.solution is not None

    def has_redundant_card(self):
        for r in combinations(self.rules, len(self.rules)-1):
            if Option(r).find_unique_solution():
                # Found a unique solution, despite ignoring a rule
                #print(f"{g}: {rule_set} IS BAD because subset {r} gives a unique solution")
                return True
        return False

    def find_unique_solution(self):
        count = 0
        for g in Guess.all_possible_guesses():
            if all(r.test(g) for r in self.rules):
                good_guess = g
                count += 1
                if count > 1:
                    return
        if count == 1:
            return good_guess


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

    def count(self, val):
        return sum(1 for d in self if d == val)

    def all_possible_guesses():
        for b,y,p in product(range(1, 6), range(1, 6), range(1, 6)):
            yield Guess(b, y, p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A Turing Machine game analyser")
    parser.add_argument("-c", "--cards", help="A comma-separated list of the cards in the game", required=True)
    args = parser.parse_args()
    try:
        cards = [int(c) for c in args.cards.split(",")]
    except ValueError:
        print("Cards must be numeric values, separated by commas")
        sys.exit(1)

    # Do we know all the rules needed?
    not_got = [c for c in cards if c not in card_rules]
    if not_got:
        print(f"I don't have cards {not_got}")
        sys.exit(1)

    solve_for_cards(cards)
