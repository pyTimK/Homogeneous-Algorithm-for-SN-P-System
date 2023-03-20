from copy import deepcopy
from src.classes.rule_transition_set import RuleTransitionSet
from src.classes.partition_events_set import PartitionEventsSet
from src.classes.partition_events import PartitionEvents
from src.classes.period_constants_pair import PeriodConstantsPair
from .partition_events_set import partition_events_set

#! ALGORITHM 2
def compatible(R: RuleTransitionSet, R_prime: RuleTransitionSet) -> bool:
    print(f"Compatible({R}, {R_prime})")
    R_bounded = R.get_bounded()
    R_unbounded = R.get_unbounded()
    R_prime_bounded = R_prime.get_bounded()
    R_prime_unbounded = R_prime.get_unbounded()
    # print(f"R_bounded: {R_bounded}")
    # print(f"R_unbounded: {R_unbounded}")
    # print(f"R_prime_bounded: {R_prime_bounded}")
    # print(f"R_prime_unbounded: {R_prime_unbounded}")
    

    # For bounded
    P = partition_events_set(R_bounded, bounded=True)
    P_prime = partition_events_set(R_prime_bounded, bounded=True)
    print(f"P: {P}")
    print(f"P': {P_prime}")
    csp = PeriodConstantsPair.intersection_bounded(P.scope(), P_prime.scope())
    print(f"csp: {csp}")
    P_bar = PartitionEventsSet({PartitionEvents(PeriodConstantsPair.intersection_bounded(pe.block, csp), deepcopy(pe.events)) for pe in P if not PeriodConstantsPair.intersection_bounded(pe.block, csp).is_empty()})
    print(f"P_bar: {P_bar}")
    P_bar_prime = PartitionEventsSet({PartitionEvents(PeriodConstantsPair.intersection_bounded(pe.block, csp), deepcopy(pe.events)) for pe in P_prime if not PeriodConstantsPair.intersection_bounded(pe.block, csp).is_empty()})
    print(f"P_bar': {P_bar_prime}")
    is_compatible = P_bar == P_bar_prime
    print(f"Compatible bounded? {is_compatible}")
    if not is_compatible:
        return False

    # For unbounded
    P = partition_events_set(R_unbounded)
    P_prime = partition_events_set(R_prime_unbounded)
    print(f"P: {P}")
    print(f"P': {P_prime}")
    print(f"P_prime.scope(): {P_prime.scope()}")
    csp = PeriodConstantsPair.intersection_unbounded(P.scope(), P_prime.scope())
    print(f"csp: {csp}")
    P_bar = PartitionEventsSet({PartitionEvents(PeriodConstantsPair.intersection_unbounded(pe.block, csp), deepcopy(pe.events)) for pe in P if not PeriodConstantsPair.intersection_unbounded(pe.block, csp).is_empty()})
    print(f"P_bar: {P_bar}")
    P_bar_prime = PartitionEventsSet({PartitionEvents(PeriodConstantsPair.intersection_unbounded(pe.block, csp), deepcopy(pe.events)) for pe in P_prime if not PeriodConstantsPair.intersection_unbounded(pe.block, csp).is_empty()})
    print(f"P_bar': {P_bar_prime}")
    is_compatible = P_bar == P_bar_prime
    print(f"Compatible unbounded? {is_compatible}")

    return is_compatible
