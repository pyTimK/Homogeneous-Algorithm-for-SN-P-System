import itertools
from typing import Set
from .period_constants_pair import PeriodConstantsPair
from .rule_transition import RuleTransition
from copy import deepcopy

class RuleTransitionSet(set[RuleTransition]):
    def powerset(self) -> Set["RuleTransitionSet"]:
        return set({RuleTransitionSet(x) for x in itertools.chain.from_iterable(itertools.combinations(self, r) for r in range(len(self) + 1))})


    def scope(self):
        return PeriodConstantsPair.union_unbounded(*[rt.state for rt in self])
    

    def union(self, *rts2_tuple: "RuleTransitionSet"):
        return RuleTransitionSet(super().union(*rts2_tuple))
    
    def get_bounded(self):
        return RuleTransitionSet({rt for rt in self if rt.state.period == 0})
    
    def get_unbounded(self):
        return RuleTransitionSet({rt for rt in self if rt.state.period != 0})


    def minimized_union(self, rts2: "RuleTransitionSet"):
        rts_bounded = self.get_bounded()
        rts_unbounded = self.get_unbounded()
        rts2_bounded = rts2.get_bounded()
        rts2_unbounded = rts2.get_unbounded()

        # For bounded
        rtsU_bounded = rts_bounded.union(rts2_bounded)
        EV_bounded = {rt.event for rt in rtsU_bounded}
        rtsMin_bounded = RuleTransitionSet()

        for event in EV_bounded:
            s = PeriodConstantsPair.union_bounded(*[rt.state for rt in rtsU_bounded if rt.event == event])
            rtsMin_bounded.add(RuleTransition(s, deepcopy(event)))


        # For unbounded
        rtsU_unbounded = rts_unbounded.union(rts2_unbounded)
        EV_unbounded = {rt.event for rt in rtsU_unbounded}
        rtsMin_unbounded = RuleTransitionSet()

        for event in EV_unbounded:
            s = PeriodConstantsPair.union_unbounded(*[rt.state for rt in rtsU_unbounded if rt.event == event])
            rtsMin_unbounded.add(RuleTransition(s, deepcopy(event)))

        return rtsMin_bounded.union(rtsMin_unbounded)


    def scale(self, x: int):
        return RuleTransitionSet({rt.scale(x) for rt in self})


    def translate(self, x: int):
        return RuleTransitionSet({rt.translate(x) for rt in self})

    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)
