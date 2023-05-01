from src.classes.snp_system import SnpSystem
from src.classes.rule_set import RuleSet
from src.classes.neuron import Neuron
from typing import Dict

#! ALGORITHM 1
def homogenize(snp_system: SnpSystem) -> RuleSet:
    """
    Turns a general SN P system to a Homogenized SN P system

    Complexity: `O((n^2)k + nt)`
    """
    rule_sets = snp_system.get_rule_sets()  #! O(n)

    p = len(rule_sets)  #! O(1)

    if p == 0:  #! O(1)
        raise ValueError("Not a single rule is given")  #! O(1)
    

    if p == 1:  #! O(1)
        return rule_sets.pop()  #! O(1)
    
    # Used to remember the translate param of a neuron
    neuron_to_translate_param: Dict[Neuron, int] = {}  #! O(1)
    
    # Used to remember all j of multiplier neurons (aj -> aj)

    #! Step 1
    i = 0  #! O(1)
    R: RuleSet = RuleSet({})  #! O(1)
    for R_prime in rule_sets:  #! O(n)

        R_scaled = R_prime.scale(p)  #! O(nk)
        R_translated = R_scaled.translate(i)  #! O(nk)
        R = R.union(R_translated)  #! O((n^2)k)

        # Used to remember the translate param of a neuron
        for neuron in snp_system.neurons:  #! O(n^2)
            if neuron.rules == R_prime:  #! O(n^2)
                neuron_to_translate_param[neuron] = i  #! O(n^2)

        i+=1  #! O(n)


    #! Step 2-3: Scale Neurons
    for neuron in snp_system.neurons:  #! O(n)
        neuron.scale(p)  #! O(n(k + t))


    #! Step 4: Translate Neurons
    for neuron in snp_system.neurons:  #! O(n)
        t = neuron_to_translate_param.get(neuron, 0)  #! O(n)
        neuron.translate(t)  #! O(nk)
    



    #! Step 5
    for neuron in snp_system.neurons:  #! O(n)
        neuron.rules = R  #! O(n)

    return R  #! O(1)
