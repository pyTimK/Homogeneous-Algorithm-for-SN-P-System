from collections import OrderedDict
from typing import Any, List, Set
from rule import RuleSet
from neuron import Neuron
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
            

        
    def get_rule_sets(self):
        """Returns a set of unique rule sets"""
        return set({neuron.rules for neuron in self.neurons if len(neuron.rules) > 0})

    def get_neuron_subsystem(self, neuron: Neuron) -> Set[Neuron]:
        subsystem: List[Neuron] = []
        for neuron_prime in self.neurons:
            if neuron_prime == neuron:
                continue

            if neuron.id in neuron_prime.out:
                subsystem.append(neuron_prime)
        
        return subsystem

    def type_2_subsystem_scaling(self, neuron: Neuron, x: int) -> Set[int]:
        # TYPE 2 - SUBSYSTEM SCALING
        subsystem = self.get_neuron_subsystem(neuron)

        multipliers: Set[int] = set()

        for neuron_prime in subsystem:
            # 1. Create multiplier neurons and Connect it to the selected neuron
            for i in range(x):
                multiplier_neuron, new_multipliers = Neuron.multiplier_neuron(neuron_prime, neuron, i)
                self.neurons.append(multiplier_neuron)
                multipliers.update(new_multipliers)

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

        return multipliers


    def to_xmp(self):
        snp_system_dict = {
            "content": {}
        }

        for neuron in self.neurons:
            if neuron.is_output:
                neuron_dict = {
                    "id": neuron.id,
                    "position": {
                        "x": neuron.position.x,
                        "y": neuron.position.y,
                    },
                    "isOutput": neuron.is_output,
                    "isInput": neuron.is_input,
                    "spikes": 0,
                    "bitstring": "",
                }
            
            else:
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


            snp_system_dict["content"][neuron.id] = neuron_dict

        xml_str = xmltodict.unparse(snp_system_dict, pretty=True)
        xml_str = '\n'.join(xml_str.split('\n')[1:])

        return xml_str


