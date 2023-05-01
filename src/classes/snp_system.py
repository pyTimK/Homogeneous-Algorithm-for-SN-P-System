from collections import OrderedDict
from typing import Any, List, Set
import xmltodict
from .neuron import Neuron
from src.types.snp_system_dict import SnpSystemDict

#! SNP SYSTEM
class SnpSystem:
    """Main class for SN P systems"""

    def __init__(self, neurons: List[Neuron]):
        """
        Initializes an SnpSystem

        Complexity: `O(1)`
        """
        self.neurons = neurons  #! O(1)
        
        
    def get_rule_sets(self):
        """
        Returns a set of unique rule sets

        Complexity: `O(n)`
        """
        return set({neuron.rules for neuron in self.neurons if len(neuron.rules) > 0})  #! O(n)
    
    def get_input_neurons(self):
        """
        Returns a list of all input neurons
        
        Complexity: `O(n)`
        """
        return [neuron for neuron in self.neurons if neuron.is_input] #! O(n)
    
    def get_output_neurons(self):
        """
        Returns a list of all output neurons
        
        Complexity: `O(n)`
        """
        return [neuron for neuron in self.neurons if neuron.is_output] #! O(n)

    def get_non_input_and_non_output_neurons(self):
        """
        Returns a list of all non-input and non-output neurons
        
        Complexity: `O(n)`
        """
        return [neuron for neuron in self.neurons if not (neuron.is_input or neuron.is_output)] #! O(n)



    def get_neuron_subsystem(self, neuron: Neuron) -> Set[Neuron]:
        """
        returns all neurons connected to the given neuron

        NOTE: not included when using the type-3-subsystem scaling
        """
        subsystem: List[Neuron] = []
        for neuron_prime in self.neurons:
            if neuron_prime == neuron:
                continue

            if neuron.id in neuron_prime.out:
                subsystem.append(neuron_prime)
        
        return subsystem

    def type_2_subsystem_scaling(self, neuron: Neuron, x: int) -> Set[int]:
        """
        TYPE 2 - SUBSYSTEM SCALING

        NOTE: not included when using the type-3-subsystem scaling
        """
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


    #! Parsing
    @staticmethod
    def from_dict(snp_system_dict: SnpSystemDict):
        """
        Converts the input SN P System dictionary to its equivalent SnpSystem object

        Complexity: `O(n^2 + nk + nt)`
        """

        content_dict = snp_system_dict.get("content")  #! O(1)

        if content_dict == None:  #! O(1)
            raise ValueError("Input SNP System xmp file does not contain `content` key")  #! O(1)
        
        return SnpSystem([Neuron.from_dict(neuron_dict) for neuron_dict in content_dict.values()])  #! O(n^2 + nk + nt)
    

    def to_xmp(self):
        """
        Converts the Snp_system object to its equivalent xmp string
        """
        content = {}
        for neuron in self.neurons:
            neuron_xmp = neuron.to_xmp()
            content[neuron.id] = neuron_xmp

        snp_system_xmp = {"content": content}
        xml_str = xmltodict.unparse(snp_system_xmp, pretty=True)
        xml_str = '\n'.join(xml_str.split('\n')[1:])

        return xml_str


