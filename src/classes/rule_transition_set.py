import itertools
from typing import Set
from .rule_transition import RuleTransition
from copy import deepcopy

class RuleTransitionSet(set[RuleTransition]):
    def powerset(self) -> Set["RuleTransitionSet"]:
        return RuleTransitionSet(set([set(x) for x in itertools.chain.from_iterable(itertools.combinations(self, r) for r in range(len(self) + 1))]))

    def scale(self, x: int):
        return RuleTransitionSet({rt.scale(x) for rt in self})

    def translate(self, x: int):
        return RuleTransitionSet({rt.translate(x) for rt in self})


