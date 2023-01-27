from typing import Set
from src.classes.snp_system import Snp_system
from src.classes.rule_transition_set import RuleTransitionSet
from .match import match

#! ALGORITHM 5
def homogenize(snp_system: Snp_system) -> Set[RuleTransitionSet]:
    rule_transition_sets = snp_system.get_set_of_rule_transition_set()
    
    if len(rule_transition_sets) == 0:
        raise ValueError("Not a single rule is given")
    
    if len(rule_transition_sets) == 1:
        return rule_transition_sets

    R = rule_transition_sets.pop()

    for R_prime in rule_transition_sets:
        u1, t1, u2, t2 = match(R, R_prime)

        
        R_double_prime = R.scale(u1).translate(t1).minimized_union(R_prime.scale(u2).translate(t2))

        
        for neuron in snp_system.neurons:
            # Neurons containing rule sets represented by R is translated by t1 
            # while their subsystems are type-2 scaled by a factor of u1.;
            if neuron.rule_transition_set == R:
                neuron.translate(t1)
                neuron.scale(u1)
                snp_system.type_2_subsystem_scaling(neuron, u1)


                # The rule set of the neurons that initially contains rules represented
                # by R will be replaced by the new common rule set represented by R′′;
                neuron.rule_transition_set = R_double_prime

            # Neurons containing rule sets represented by R′ is translated by t2
            # while their subsystems are type-2 scaled by a factor of u2.;
            elif neuron.rule_transition_set == R_prime:
                neuron.translate(t2)
                neuron.scale(u2)
                snp_system.type_2_subsystem_scaling(neuron, u2)

                # The rule set of the neurons that initially contains rules represented
                # by R′ will be replaced by the new common rule set represented by R′′;
                neuron.rule_transition_set = R_double_prime


        R = R_double_prime
    
    return R


    # print(rule_transition_sets_input)


        # u1, t1, u2, t2 = 2, 1, 2, 0
        # print(u1, t1, u2, t2)
        # print("R")
        # print(R)
        # print(R.scale(u1).translate(t1))
        # print("R'")
        # print(R_prime)
        # print(R_prime.scale(u2).translate(t2))



                        











