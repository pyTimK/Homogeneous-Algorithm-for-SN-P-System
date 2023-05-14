from src.classes.snp_system import SnpSystem
from src.classes.rule_set import RuleSet
from src.classes.neuron import Neuron
from typing import Dict

#! ALGORITHM 1
def modified_homogenize(snp_system: SnpSystem) -> RuleSet:
    """
    Turns a general SN P system to a Homogenized SN P system

    Complexity: `O(nk)`
    """

    #! Step 1: Get set of unique rule sets
    rule_sets = snp_system.get_unique_rule_sets()  #! O(nk)

    p = len(rule_sets)  #! O(1)

    if p == 0:  #! O(1)
        raise ValueError("Not a single rule is given")  #! O(1)
    

    if p == 1:  #! O(1)
        return rule_sets.pop()  #! O(1)
    
    # Used to remember the translate param of a rule set
    rule_set_to_translate_param: Dict[RuleSet, int] = {}  #! O(1)
    
    

    #! Step 2: R <- (pR1+0) U (pR2+1) U ... U (pRp + (p-1))
    i = 0  #! O(1)
    R: RuleSet = RuleSet({})  #! O(1)
    for R_prime in rule_sets:  #! O(n)

        R_scaled = R_prime.scale(p)  #! O(nk)
        R_translated = R_scaled.translate(i)  #! O(nk)
        # R = R.union(R_translated)  # O((n^2)k)
        R.update(R_translated) #! O(nk)

        # Used to remember the translate param of a rule set
        rule_set_to_translate_param[R_scaled] = i  #! O(n)

        i+=1  #! O(n)


    #! Step 3: Scale Neurons
    for neuron in snp_system.neurons:  #! O(n)
        neuron.scale(p)  #! O(nk)


    #! Step 4: Translate Neurons
    print(rule_set_to_translate_param)
    for neuron in snp_system.neurons:  #! O(n)
        t = rule_set_to_translate_param.get(neuron.rules, 0)  #! O(n)
        neuron.translate(t)  #! O(nk)
    



    #! Step 5
    for neuron in snp_system.neurons:  #! O(n)
        neuron.rules = R  #! O(n)

    return R  #! O(1)
