from collections import OrderedDict
from typing import Any, List, Set
from .rule import Rule
from .neuron import Neuron

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

    
    def get_rules(self) -> List[Rule]:
        return list(itertools.chain.from_iterable([neuron.rules for neuron in self.neurons]))
        
    def get_unique_rules(self) -> Set[Rule]:
        return set(self.get_rules())
        
        # rules = self.get_rules()
        # unique_rules: Set[Rule] = set()

        # for r1 in rules:
        #     for r2 in unique_rules:
        #         if r1
        





