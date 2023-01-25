from typing import Set, Tuple
from copy import deepcopy
from src.classes.my_math import MyMath
from src.classes.rule_transition import RuleTransition
from src.classes.rule_transition_set import RuleTransitionSet
from src.classes.period_constants_pair import PeriodConstantsPair
from src.classes.constants import Constants
from src.classes.parition_events_set import PartitionEventsSet

#! ALGORITHM 5
def homogenize(rules_input: RuleTransitionSet) -> RuleTransitionSet:

    rules = deepcopy(rules_input)
    if len(rules) == 0:
        raise ValueError("Not a single rule is given")
    
    if len(rules) == 1:
        return rules

    R = rules.pop()

    for R_prime in rules:
        u1, t1, u2, t2 = match(R, R_prime)



#! ALGORITHM 4
def match(R: RuleTransitionSet, R_prime: RuleTransitionSet) -> Tuple[int, int, int, int]:
    for r in R:
        for r_prime in R_prime:

            s = r.state
            alpha = r.event.alpha
            beta = r.event.beta

            s_prime = r_prime.state
            alpha_prime = r_prime.event.alpha
            beta_prime = r_prime.event.beta

            if beta != beta_prime:
                continue

            else:
                l = MyMath.lcm(abs(alpha), abs(alpha_prime))
                m1 = l // abs(alpha)
                m2 = l // abs(alpha_prime)

                u1_prime, t1, u2_prime, t2 = get_parameters(s.scale(m1), s_prime.scale(m2))
                u1, t1, u2, t2 = u1_prime * m1, t1, u2_prime * m2, t2

                if t1 == -1 or t2 == -1:
                    continue

                else:
                    if compatible(R.scale(u1).translate(t1), R.scale(u2).translate(t2)):
                        return u1, t1, u2, t2
                    
                    else:
                        continue

    return 2, 0, 2, 1
                        



#! ALGORITHM 3
def get_parameters(s: PeriodConstantsPair, s_prime: PeriodConstantsPair) -> Tuple[int, int, int, int]:
    l, q_bar, q_bar_prime = s.get_combine_params(s_prime)

    if len(q_bar) <= len(q_bar_prime):
        u1, t1, u2, t2 = -1, -1, 1, 0

        for u1_prime in range(1, l + 2):
            for t1_prime in range(0, l):

                q_double_bar_prime = Constants()
                for l_mult in range(0, (u1_prime - 1) * l + 1, l):
                    for q_bar_prime_item in q_bar_prime:
                        q_double_bar_prime.add(q_bar_prime_item + l_mult)
                
                if q_bar.scale(u1_prime).translate(t1_prime).mod(l).issubset(q_double_bar_prime):
                    u1, t1, u2, t2 = u1_prime, t1_prime, u2, t2
                    return u1, t1, u2, t2

    else:
        u1, t1, u2, t2 = 1, 0, -1, -1

        for u2_prime in range(1, l + 2):
            for t2_prime in range(0, l):

                q_double_bar = Constants()
                for l_mult in range(0, (u2_prime - 1) * l + 1, l):
                    for q_bar_item in q_bar:
                        q_double_bar.add(q_bar_item + l_mult)
                
                if q_bar_prime.scale(u2_prime).translate(t2_prime).mod(l).issubset(q_double_bar):
                    u1, t1, u2, t2 = u1, t1, u2_prime, t2_prime
                    return u1, t1, u2, t2

    return u1, t1, u2, t2


#! ALGORITHM 2
def compatible(R: RuleTransitionSet, R_prime: RuleTransitionSet):
    P = partition_events_set(R)
    P_prime = partition_events_set(R_prime)
    # csp = TODO continue


#! ALGORITHM 1
def partition_events_set(R: RuleTransitionSet) -> Set[PartitionEventsSet]:
    P0: Set[PartitionEventsSet] = set()
    P: Set[PartitionEventsSet] = set()

    for T in R.powerset():
        T_prime = R - T
        S = {rule_transition.state for rule_transition in T}
        S_prime = {rule_transition.state for rule_transition in T_prime}
        E_prime = {rule_transition.event for rule_transition in T}
        b_prime = PeriodConstantsPair.intersection(S) - PeriodConstantsPair.union(S_prime)

        if not b_prime.is_empty:
            P0.add(PartitionEventsSet(b_prime, E_prime))
        
    EV = {partition_events.events for partition_events in P0}

    for events in EV:
        b = PeriodConstantsPair.union([pes.block for pes in P0 if pes.events == events])
        P.add(b, deepcopy(events))
    
    return P


