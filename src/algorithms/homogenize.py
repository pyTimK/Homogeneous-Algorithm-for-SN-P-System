from typing import Set
from copy import deepcopy
from src.classes.rule_transition_set import RuleTransitionSet
from .match import match

#! ALGORITHM 5
def homogenize(rule_transition_sets_input: Set[RuleTransitionSet]) -> Set[RuleTransitionSet]:
    # print(rule_transition_sets_input)
    rule_transition_sets = deepcopy(rule_transition_sets_input)
    if len(rule_transition_sets) == 0:
        raise ValueError("Not a single rule is given")
    
    if len(rule_transition_sets) == 1:
        return rule_transition_sets

    R = rule_transition_sets.pop()

    for R_prime in rule_transition_sets:
        u1, t1, u2, t2 = match(R, R_prime)
        # u1, t1, u2, t2 = 2, 1, 2, 0
        # print(u1, t1, u2, t2)
        # print("R")
        # print(R)
        # print(R.scale(u1).translate(t1))
        # print("R'")
        # print(R_prime)
        # print(R_prime.scale(u2).translate(t2))
        
        R_double_prime = R.scale(u1).translate(t1).minimized_union(R_prime.scale(u2).translate(t2))

        # TODO
        # Neurons containing rule sets represented by R is translated by t1 
        # while their subsystems are type-2 scaled by a factor of u1.;

        # TODO
        # Neurons containing rule sets represented by R′ is translated by t2
        # while their subsystems are type-2 scaled by a factor of u2.;

        # TODO
        # The rule set of the neurons that initially contains rules represented
        # by R or R′ will be replaced by the new common rule set
        # represented by R′′;

        R = R_double_prime
    
    return R






                        











