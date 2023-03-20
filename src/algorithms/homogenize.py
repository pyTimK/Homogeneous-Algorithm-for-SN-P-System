from src.classes.snp_system import Snp_system
from src.classes.rule import Rule, RuleSet
from src.classes.rule_re import RuleRE, StarExpSet, PlusExpSet
from copy import copy
from src.classes.neuron import Neuron
from typing import Dict, Set

#! ALGORITHM 5
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
    multipliers: Set[int] = set()

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

    nonmultiplier_neurons = [neuron for neuron in copy(snp_system.neurons) if not neuron.is_input and not neuron.is_output]
    #! Step 2
    for neuron in nonmultiplier_neurons:
        neuron.scale(p)
        multipliers.update(snp_system.type_2_subsystem_scaling(neuron, p))


    #! Step 3
    for neuron in nonmultiplier_neurons:
        neuron.translate(neuron_to_translate_param[neuron])


    #! Step 4
    R0 = RuleSet({Rule(
        rule_re = RuleRE({(spike_produced, StarExpSet({}), PlusExpSet({}))}), 
        consume = spike_produced, 
        release = spike_produced, 
        delay = 0, 
        ) for spike_produced in multipliers})



    #! Step 5
    t = 0 if len(multipliers) == 0 else max(multipliers) + 1

    #! Step 6
    R = R0.union(R.translate(t))

    #! Step 7
    for neuron in nonmultiplier_neurons:
        neuron.translate(t)

    #! Step 8
    for neuron in snp_system.neurons:
        neuron.rules = R

    return R




                        











