from src.classes.snp_system import Snp_system
from src.classes.rule import Rule, RuleSet
from src.classes.rule_re import RuleRE, StarExpSet, PlusExpSet
from copy import copy
from src.classes.neuron import Neuron
from typing import Dict, Set

#! ALGORITHM 1
def homogenize(snp_system: Snp_system) -> RuleSet:
    rule_sets = snp_system.get_rule_sets()


    p = len(rule_sets)
    
    if p == 0:
        raise ValueError("Not a single rule is given")
    

    if p == 1:
        return rule_sets.pop()
    
    # Used to remember the translate param of a neuron
    neuron_to_translate_param: Dict[Neuron, int] = {}
    
    # Used to remember all j of multiplier neurons (aj -> aj)

    #! Step 1
    i = 0
    R: RuleSet = RuleSet({})
    for R_prime in rule_sets:
        R = R.union(R_prime.scale(p).translate(i))

        # Used to remember the translate param of a neuron
        for neuron in snp_system.neurons:
            if neuron.rules == R_prime:
                neuron_to_translate_param[neuron] = i

        i+=1

    non_input_output_neurons = [neuron for neuron in copy(snp_system.neurons) if not neuron.is_input and not neuron.is_output]
    # output_neuron = next(filter(lambda neuron: neuron.is_output, snp_system.neurons), None)
    # neuron_connected_to_output_neuron = next(filter(lambda neuron: output_neuron.id in neuron.out, non_input_output_neurons), None)

    #! Step 2
    for neuron in non_input_output_neurons:
        print(f"{neuron.id}, {neuron.spikes} is scaled by {p}")
        neuron.scale(p)


    #! Step 3
    for neuron in non_input_output_neurons:
        t = neuron_to_translate_param[neuron]
        print(f"{neuron.id} is translated by {t}")
        neuron.translate(t)



    #! Step 8
    for neuron in snp_system.neurons:
        neuron.rules = R

    return R
