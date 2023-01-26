from copy import deepcopy
from src.classes.rule_transition_set import RuleTransitionSet
from src.classes.partition_events_set import PartitionEventsSet
from src.classes.partition_events import PartitionEvents
from .partition_events_set import partition_events_set

#! ALGORITHM 2
def compatible(R: RuleTransitionSet, R_prime: RuleTransitionSet) -> bool:
    P = partition_events_set(R)
    P_prime = partition_events_set(R_prime)
    csp = P.scope().intersection(P_prime.scope())
    P_bar = PartitionEventsSet({PartitionEvents(pe.block.intersection(csp), deepcopy(pe.events)) for pe in P if not pe.block.intersection(csp).is_empty()})
    P_bar_prime = PartitionEventsSet({PartitionEvents(pe.block.intersection(csp), deepcopy(pe.events)) for pe in P_prime if not pe.block.intersection(csp).is_empty()})
    return P_bar == P_bar_prime
