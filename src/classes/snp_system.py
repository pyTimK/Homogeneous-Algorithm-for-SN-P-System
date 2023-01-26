from collections import OrderedDict
from typing import Any, List, Set
from .rule import Rule
from .neuron import Neuron
from .rule_transition import RuleTransition
from .rule_transition_set import RuleTransitionSet

import itertools

#! SNP SYSTEM
class Snp_system:
    """Main class for SN P systems"""

    def __init__(self, input_json: OrderedDict[str, Any]) -> None:
        self.neurons: List[Neuron]= []

        content_json = input_json["content"]
        neuron_ids = list(content_json.keys())

        for neuron_id in neuron_ids:
            neuron_json: OrderedDict[str, Any] = content_json[neuron_id]
            self.neurons.append(Neuron(neuron_json))

    
    def get_rule_list(self) -> List[Rule]:
        return list(itertools.chain.from_iterable([neuron.rules for neuron in self.neurons]))
        
    def get_rule_set(self) -> Set[Rule]:
        return set(self.get_rule_list())

    def get_rule_transition_list(self) -> List[RuleTransition]:
        return [rule.rule_transition for rule in self.get_rule_list()]
        
    def get_rule_transition_set(self) -> RuleTransitionSet:
        return set(self.get_rule_transition_list())

        




