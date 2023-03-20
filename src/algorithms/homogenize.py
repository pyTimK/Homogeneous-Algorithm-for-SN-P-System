from typing import Set
from src.classes.snp_system import Snp_system
from src.classes.rule_transition_set import RuleTransitionSet
from src.classes.rule import Rule
from .match import match
from copy import copy, deepcopy

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
        print(f"final: {u1}, {t1}, {u2}, {t2}")

        # print(f"R_prime: {R_prime}")
        # print(f"R: {R}")

        
        R_double_prime = R.scale(u1).translate(t1).minimized_union(R_prime.scale(u2).translate(t2))
        # print(f"R_double_prime: {R_double_prime}")

        for neuron in copy(snp_system.neurons):
            # Neurons containing rule sets represented by R is translated by t1 
            # while their subsystems are type-2 scaled by a factor of u1.;
            if neuron.rule_transition_set == R:
                neuron.translate(t1)
                neuron.scale(u1)
                snp_system.type_2_subsystem_scaling(neuron, u1)


                # The rule set of the neurons that initially contains rules represented
                # by R will be replaced by the new common rule set represented by R′′;
                neuron.rule_transition_set = R_double_prime
                neuron.rules = [Rule.from_rule_transition(rt) for rt in neuron.rule_transition_set]

            # Neurons containing rule sets represented by R′ is translated by t2
            # while their subsystems are type-2 scaled by a factor of u2.;
            elif neuron.rule_transition_set == R_prime:
                neuron.translate(t2)
                neuron.scale(u2)
                snp_system.type_2_subsystem_scaling(neuron, u2)

                # The rule set of the neurons that initially contains rules represented
                # by R′ will be replaced by the new common rule set represented by R′′;
                neuron.rule_transition_set = R_double_prime
                neuron.rules = [Rule.from_rule_transition(rt) for rt in neuron.rule_transition_set]


        

        homogenized_neurons = [neuron for neuron in snp_system.neurons if neuron.rule_transition_set == R_double_prime]
        multiplier_neurons = [neuron for neuron in snp_system.neurons if neuron.rule_transition_set != R_double_prime]

        # Get the set of constants of forwarding rules in all multiplier neurons
        forwarding_constants = [rule.consume for neuron in multiplier_neurons for rule in neuron.rules]

        # Get the largest constant of a forwarding rule in multiplier neurons
        largest_forwarding_rule = 0 if len(forwarding_constants) == 0 else max(forwarding_constants)

        if largest_forwarding_rule > 0:
            translate_param = largest_forwarding_rule + 1

        # Translate the homogenized rule set
            R_double_prime = R_double_prime.translate(translate_param)

        # Merge the homogenized rule set with those of multiplier neurons
            for neuron in multiplier_neurons:
                R_double_prime = R_double_prime.minimized_union(neuron.rule_transition_set)

        # Translate all homogenized neurons and update new homogenized rule set
            for neuron in homogenized_neurons:
                neuron.translate(translate_param)
                neuron.rule_transition_set = R_double_prime
                neuron.rules = [Rule.from_rule_transition(rt) for rt in neuron.rule_transition_set]

        # Update new homogenized rule set in multiplier neurons
            for neuron in multiplier_neurons:
                neuron.rule_transition_set = R_double_prime
                neuron.rules = [Rule.from_rule_transition(rt) for rt in neuron.rule_transition_set]

        


        R = R_double_prime
        print(f"R'': {R}")
            



                
    
    print(f"Neurons length: {len(snp_system.neurons)}")
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



                        











