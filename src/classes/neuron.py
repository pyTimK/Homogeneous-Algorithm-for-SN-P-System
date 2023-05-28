from collections import OrderedDict
from .rule import Rule
from .rule_set import RuleSet
from .rule_re import RuleRE, StarExpSet, PlusExpSet
from .position import Position
from typing import List, Union
from src.types.neuron_dict import NeuronDict

class Neuron:
    """Represents a neuron in an SN P system"""

    def __init__(
        self, 
        id: str, 
        position: Position, 
        is_input: bool, 
        is_output: bool, 
        rules: RuleSet, 
        starting_spikes: int, 
        delay: int, 
        spikes: int, 
        out: List[str], 
        out_weights: OrderedDict[str, int],
        bitstring: List[int],
    ) -> None:
        """
        Initializes a neuron

        Complexity: `O(1)`
        """
        self.id = id  #! O(1)
        self.position = position  #! O(1)
        self.is_input = is_input  #! O(1)
        self.is_output = is_output  #! O(1)
        self.rules = rules  #! O(1)
        self.starting_spikes = starting_spikes  #! O(1)
        self.delay = delay  #! O(1)
        self.spikes = spikes  #! O(1)
        self.out = out  #! O(1)
        self.out_weights = out_weights  #! O(1)
        self.bitstring = bitstring  #! O(1)

    
    #! Operations
    @staticmethod
    def multiplier_neuron(neuron_prime: "Neuron", neuron: "Neuron", index: int):
        """
        Returns the necessary multiplier neuron

        Complexity: `O(k)`
        """

        spikes_produced = {rule.release * neuron_prime.out_weights[neuron.id] for rule in neuron_prime.rules}  #! O(k)

        return Neuron(
            id = f"{neuron_prime.id.split('-')[0]}_{neuron.id.split('-')[0]}_{index}",  #! O(1)
            position = neuron_prime.position.get_translate(30 * index, 0),  #! O(1)
            is_input = False,  #! O(1)
            is_output = False,  #! O(1)
            rules = RuleSet({Rule(
                rule_re = RuleRE({(spike_produced, StarExpSet({}), PlusExpSet({}))}),  #! O(1)
                consume = spike_produced,  #! O(1)
                release = spike_produced,  #! O(1)
                delay = 0,  #! O(1)
                ) for spike_produced in spikes_produced}),  #! O(k)

            starting_spikes = 0,  #! O(1)
            delay = 0,  #! O(1)
            spikes = 0,  #! O(1)
            out = [neuron.id],  #! O(1)
            out_weights={neuron.id: 1},  #! O(1)
            bitstring=[],  #! O(1)
        ), spikes_produced  #! O(k)
        

    def translate(self, x: int):
        """
        Translates a neuron

        Note that this operation acts on the neuron itself

        Complexity: `O(k)`
        """
        if self.is_input:  #! O(1)
            pass  #! O(1)

        elif self.is_output:  #! O(1)
            pass  #! O(1)

        else:  #! O(1)
            self.spikes += x  #! O(1)
            self.rules = RuleSet({rule.translate(x) for rule in self.rules})  #! O(k)
            print(f"{self.id} is translated by {x}")


    def scale(self, x: int, scale_release = True):
        """
        Scales a neuron

        Note that this operation acts on the neuron itself

        Complexity: `O(k)`
        """
        if self.is_input:  #! O(1)
            self.bitstring = [b * x for b in self.bitstring]  #! O(t) Note: In true SN P systems, the input neuron is not included in time analysis
            print(f"Input neuron {self.id} is scaled by {x}")
        
        elif self.is_output:  #! O(1)
            pass  #! O(1)

        else:
            self.spikes *= x  #! O(1)
            self.rules = RuleSet({rule.scale(x, scale_release) for rule in self.rules})  #! O(k)
            print(f"{self.id} is scaled by {x}")


    def get_rules_xmp_str(self):
        rules_xmp = self.rules.to_xmp()
        rule_str_list: List[str] = []

        for rule in self.rules:
            rule_str_list.append(rule.to_xmp_str())
        
        return " ".join(rule_str_list)
        

    #! Parsing
    @staticmethod
    def _out_from_dict(out_dict: Union[str, List[str], None]) -> List[str]:
        """
        Converts the out field of the input neuron dictionary to its equivalent List[str] value

        Complexity: `O(1)`
        """
        if out_dict == None:  #! O(1)
            return []  #! O(1)
        
        if type(out_dict) == str:  #! O(1)
            return [out_dict]  #! O(1)
        
        if type(out_dict) == List[str] or type(out_dict) == list:  #! O(1)
            return out_dict  #! O(1)
 

    @staticmethod
    def from_dict(neuron_dict: NeuronDict):
        """
        Converts the input neuron dictionary to its equivalent Neuron object

        Complexity: `O(n + k + t)`
        """

        id: str = neuron_dict.get("id")  #! O(1)
        position = Position.from_dict(neuron_dict.get("position"))  #! O(1)
        is_input = bool(neuron_dict.get("isInput") == "true")  #! O(1)
        is_output = bool(neuron_dict.get("isOutput") == "true")  #! O(1)
        rules = RuleSet.from_str(neuron_dict.get("rules"))  #! O(k)
        starting_spikes = int(neuron_dict.get("startingSpikes") or 0)  #! O(1)
        delay = int(neuron_dict.get("delay") or 0)  #! O(1)
        spikes = int(neuron_dict.get("spikes") or 0)  #! O(1)
        out = Neuron._out_from_dict(neuron_dict.get("out"))  #! O(n)
        _out_weights_str: OrderedDict[str, str] = neuron_dict.get("outWeights") or {}  #! O(n)
        out_weights: OrderedDict[str, int] =  {k: int(v) for k, v in _out_weights_str.items()}  #! O(n)
        bitstring: List[int] = [] if neuron_dict.get("bitstring") == None else [int(b) for b in str(neuron_dict.get("bitstring")).split(",")]  #! O(t)

        return Neuron(id, position, is_input, is_output, rules, starting_spikes, delay, spikes, out, out_weights, bitstring)  #! O(1)


    def to_xmp(self):
        """
        Converts the Neuron object to its equivalent xmp string
        """

        if self.is_output:
            return {
                "id": self.id,
                "position": {
                    "x": self.position.x,
                    "y": self.position.y,
                },
                "isInput": False,
                "isOutput": True,
                "spikes": 0,
                "bitstring": "",
            }

        if self.is_input:
            return {
                "id": self.id,
                "position": {
                    "x": self.position.x,
                    "y": self.position.y,
                },
                "isInput": True,
                "isOutput": False,
                "spikes": 0,
                "delay": 0,
                "out": self.out,
                "bitstring": ",".join([str(b) for b in self.bitstring]),
                "outWeights": self.out_weights,
            }
        
        return {
            "id": self.id,
            "position": {
                "x": self.position.x,
                "y": self.position.y,
            },
            "rules": self.get_rules_xmp_str(),
            "startingSpikes": self.starting_spikes,
            "delay": self.delay,
            "spikes": self.spikes,
            "isOutput": self.is_output,
            "isInput": self.is_input,
            "out": self.out,
            "outWeights": self.out_weights,
        }

    #! Dunder Methods
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Neuron):
            return self.id == __o.id
        
        return False
    
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self) -> str:
        return f"{self.id} - {self.rules}"

    def __repr__(self) -> str:
        return self.__str__()