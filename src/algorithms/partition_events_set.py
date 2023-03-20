from copy import deepcopy
from src.classes.partition_events_set import PartitionEventsSet
from src.classes.rule_transition_set import RuleTransitionSet
from src.classes.period_constants_pair import PeriodConstantsPair
from src.classes.partition_events import PartitionEvents
from src.classes.event_set import EventSet
from src.errors.not_bounded_error import NotBoundedError

#! ALGORITHM 1
def partition_events_set(R: RuleTransitionSet, bounded = False) -> PartitionEventsSet:
    if bounded:
        for rt in R:
            if rt.state.period != 0:
                raise NotBoundedError()
            
    P0: PartitionEventsSet = PartitionEventsSet()
    P: PartitionEventsSet = PartitionEventsSet()
    # print(f"R: {R}")
    # print(f"powerset(R): {R.powerset()}")

    for T in R.powerset():
        # print(f"T: {T}")
        T_prime = R - T
        # print(f"T': {T_prime}")
        S = {rule_transition.state for rule_transition in T}
        S_prime = {rule_transition.state for rule_transition in T_prime}
        E_prime = {rule_transition.event for rule_transition in T}
        # print(f"Intersection: {PeriodConstantsPair.intersection(*S)}")
        # print(f"Union: {PeriodConstantsPair.union(S_prime)}")
        if bounded:
            b_prime = PeriodConstantsPair.intersection_bounded(*S).sub_bounded(PeriodConstantsPair.union_bounded(*S_prime))
        else:
            b_prime = PeriodConstantsPair.intersection_unbounded(*S).sub_unbounded(PeriodConstantsPair.union_unbounded(*S_prime))
        # print(f"b' = {b_prime}")
        # print(f"b'.is_empty = {b_prime.is_empty()}")

        if not b_prime.is_empty():
            P0.add(PartitionEvents(b_prime, EventSet(E_prime)))
        
    EV = {partition_events.events for partition_events in P0}
    # print(f"EV: {EV}")

    for events in EV:
        if bounded:
            b = PeriodConstantsPair.union_bounded(*[pes.block for pes in P0 if pes.events == events])
        else:
            b = PeriodConstantsPair.union_unbounded(*[pes.block for pes in P0 if pes.events == events])


        P.add(PartitionEvents(b, deepcopy(events)))
    
    return P