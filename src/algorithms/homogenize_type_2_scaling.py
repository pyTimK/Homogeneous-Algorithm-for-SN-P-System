from src.classes.snp_system import SnpSystem
from src.classes.rule_set import RuleSet
from src.classes.neuron import Neuron
from src.classes.rule import Rule
from src.classes.rule_re import RuleRE, StarExpSet, PlusExpSet
from typing import Dict, Set
from copy import copy

#! ALGORITHM 1
def homogenize_type_2_scaling(snp_system: SnpSystem) -> RuleSet:
    """
    Turns a general SN P system to a Homogenized SN P system

    Complexity: `O(n^2k)`
    """
    rule_sets = snp_system.get_unique_rule_sets()  #! O(nk)
 

    p = len(rule_sets)  #! O(1)

    if p == 0:  #! O(1)
        raise ValueError("Not a single rule is given")  #! O(1)
    

    if p == 1:  #! O(1)
        return rule_sets.pop()  #! O(1)
    
    # Used to remember the translate param of a rule set
    rule_set_to_translate_param: Dict[RuleSet, int] = {}  #! O(1)
    
    # Used to remember all j of multiplier neurons (aj -> aj)
    multipliers: Set[int] = set() #! O(1)

    #! Step: 1 R <- (pR1+0) U (pR2+1) U ... U (pRp + (p-1))
    i = 0  #! O(1)
    R: RuleSet = RuleSet({})  #! O(1)
    for R_prime in rule_sets:  #! O(n)

        R_scaled = R_prime.scale(p, scale_release=False)  #! O(nk)
        R_translated = R_scaled.translate(i)  #! O(nk)
        # R = R.union(R_translated)  # O((n^2)k)
        R.update(R_translated) #! O(nk)

        # Used to remember the translate param of a rule set
        rule_set_to_translate_param[R_scaled] = i  #! O(n)

        i+=1  #! O(n)

    nonmultiplier_neurons = [neuron for neuron in copy(snp_system.neurons) if not neuron.is_input and not neuron.is_output]  #! O(n)

    #! Step 2: Scale Neurons
    for neuron in nonmultiplier_neurons:  #! O(n)
        neuron.scale(p, scale_release=False)  #! O(nk)
        multipliers.update(snp_system.type_2_subsystem_scaling(neuron, p))  #! O(n^2k)

    #! Step 3: Translate Neurons
    for neuron in nonmultiplier_neurons:
        t = rule_set_to_translate_param.get(neuron.rules, 0)  #! O(n)
        neuron.translate(t)  #! O(nk)



    #! Step 4: Get union of rule sets of all multiplier neurons
    R0 = RuleSet({Rule(
        rule_re = RuleRE({(spike_produced, StarExpSet({}), PlusExpSet({}))}),  #! O(1)
        consume = spike_produced,  #! O(1)
        release = spike_produced,  #! O(1)
        delay = 0,  #! O(1)
        ) for spike_produced in multipliers})  #! O(nk)
    
    # print("R0")
    # print(R0)
    # print("multipliers")
    # print(multipliers)


    #! Step 5: Set the offset as the upper bound of the multipliers
    t = 0 if len(multipliers) == 0 else max(multipliers) + 1  #! O(1)
    # print("t")
    # print(t)
    #! Step 6: Get the final rule set
    R = R0.union(R.translate(t))  #! O(nk)

    #! Step 7: Translate all non-multiplier neurons by t
    for neuron in nonmultiplier_neurons:  #! O(n)
        neuron.translate(t)  #! O(nk)

    #! Step 8: 
    for neuron in snp_system.neurons:  #! O(n)
        neuron.rules = R  #! O(n)

    return R  #! O(1)
