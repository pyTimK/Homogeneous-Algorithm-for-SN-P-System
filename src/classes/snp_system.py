from collections import OrderedDict
from typing import Any, List, Set
from .rule import Rule
from .neuron import Neuron
from .rule_transition import RuleTransition
from .rule_transition_set import RuleTransitionSet
import xmltodict

#! SNP SYSTEM
class Snp_system:
    """Main class for SN P systems"""

    def __init__(self, input_json: OrderedDict[str, Any]) -> None:
        self.neurons: List[Neuron]= []

        content_json = input_json["content"]
        neuron_ids = list(content_json.keys())

        for neuron_id in neuron_ids:
            neuron_json: OrderedDict[str, Any] = content_json[neuron_id]
            neuron = Neuron.from_neuron_json(neuron_json)
            self.neurons.append(neuron)
            

        
    def get_set_of_rule_transition_set(self) -> Set[RuleTransitionSet]:
        return {neuron.rule_transition_set for neuron in self.neurons}

    def get_neuron_subsystem(self, neuron: Neuron) -> Set[Neuron]:
        subsystem: List[Neuron] = []
        for neuron_prime in self.neurons:
            if neuron_prime == neuron:
                continue

            if neuron.id in neuron_prime.out:
                subsystem.append(neuron_prime)
        
        return subsystem

    def type_2_subsystem_scaling(self, neuron: Neuron, x: int):
        # TYPE 2 - SUBSYSTEM SCALING
        subsystem = self.get_neuron_subsystem(neuron)

        for neuron_prime in subsystem:
            # 1. Create multiplier neurons and Connect it to the selected neuron
            for i in range(x):
                multiplier_neuron = Neuron.multiplier_neuron(neuron_prime, neuron, i)
                self.neurons.append(multiplier_neuron)

                # 2. Connect the subsystem neuron to multiplier neurons
                neuron_prime.out.append(multiplier_neuron.id)
                # print(f"multiplier_neuron.id:{multiplier_neuron.id}")
                # print(f"neuron_prime.out: {neuron_prime.out}")
                neuron_prime.out_weights[multiplier_neuron.id] = 1
            
            # 3. Disconnect the subsystem neuron to the selected neuron
            if neuron.id in neuron_prime.out:
                neuron_prime.out.remove(neuron.id)
            
            if neuron.id in neuron_prime.out_weights:
                del neuron_prime.out_weights[neuron.id]


    def to_xmp(self):
        snp_system_dict = {
            "content": {}
        }

        for neuron in self.neurons:
            neuron_dict = {
                "id": neuron.id,
                "position": {
                    "x": neuron.position.x,
                    "y": neuron.position.y,
                },
                "rules": neuron.get_rules_xmp_str(),
                "startingSpikes": neuron.starting_spikes,
                "delay": neuron.delay,
                "spikes": neuron.spikes,
                "isOutput": neuron.is_output,
                "isInput": neuron.is_input,
                "out": neuron.out,
                "outWeights": neuron.out_weights
            }
            # print(f"neuron.out: {neuron.out}")

            # if len(neuron.out) > 0:
            #     print(neuron.out)
            #     neuron_dict["out"] = " ".join(neuron.out)
            

            snp_system_dict["content"][neuron.id] = neuron_dict

        xml_str = xmltodict.unparse(snp_system_dict, pretty=True)
        xml_str = '\n'.join(xml_str.split('\n')[1:])

        return xml_str


