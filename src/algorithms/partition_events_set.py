from copy import deepcopy
from src.classes.partition_events_set import PartitionEventsSet
from src.classes.rule_transition_set import RuleTransitionSet
from src.classes.period_constants_pair import PeriodConstantsPair
from src.classes.partition_events import PartitionEvents

#! ALGORITHM 1
def partition_events_set(R: RuleTransitionSet) -> PartitionEventsSet:
    P0: PartitionEventsSet = PartitionEventsSet()
    P: PartitionEventsSet = PartitionEventsSet()

    for T in R.powerset():
        T_prime = R - T
        S = {rule_transition.state for rule_transition in T}
        S_prime = {rule_transition.state for rule_transition in T_prime}
        E_prime = {rule_transition.event for rule_transition in T}
        # print(f"Intersection: {PeriodConstantsPair.intersection(*S)}")
        # print(f"Union: {PeriodConstantsPair.union(S_prime)}")
        b_prime = PeriodConstantsPair.intersection(*S) - PeriodConstantsPair.union(*S_prime)

        if not b_prime.is_empty:
            P0.add(PartitionEvents(b_prime, E_prime))
        
    EV = {partition_events.events for partition_events in P0}

    for events in EV:
        b = PeriodConstantsPair.union(*[pes.block for pes in P0 if pes.events == events])
        P.add(b, deepcopy(events))
    
    return P