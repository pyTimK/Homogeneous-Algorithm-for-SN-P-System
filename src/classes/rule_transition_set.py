import itertools
from typing import Set
from .period_constants_pair import PeriodConstantsPair
from .rule_transition import RuleTransition
from copy import deepcopy

class RuleTransitionSet(set[RuleTransition]):
    def powerset(self) -> Set["RuleTransitionSet"]:
        return set({RuleTransitionSet(x) for x in itertools.chain.from_iterable(itertools.combinations(self, r) for r in range(len(self) + 1))})


    def scope(self):
        return PeriodConstantsPair.union(*[rt.state for rt in self])
    

    def union(self, *rts2_tuple: "RuleTransitionSet"):
        return RuleTransitionSet(super().union(*rts2_tuple))


    def minimized_union(self, *rts2: "RuleTransitionSet"):
        rtsU = self.union(*rts2)
        EV = {rt.event for rt in rtsU}
        rtsMin = RuleTransitionSet()

        for event in EV:
            s = PeriodConstantsPair.union(*[rts.state for rts in rtsU if rts.event == event])
            rtsMin.add(RuleTransition(s, deepcopy(event)))

        return rtsMin


    def scale(self, x: int):
        return RuleTransitionSet({rt.scale(x) for rt in self})


    def translate(self, x: int):
        return RuleTransitionSet({rt.translate(x) for rt in self})

    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)
