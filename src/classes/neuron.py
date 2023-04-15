from collections import OrderedDict
from rule import Rule, RuleSet
from rule_re import RuleRE, StarExpSet, PlusExpSet
from position import Position
from typing import Any, List

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
        out_weights: OrderedDict[str, int]
    ) -> None:
        self.id = id
        self.position = position
        self.is_input = is_input
        self.is_output = is_output
        self.rules = rules
        self.starting_spikes = starting_spikes
        self.delay = delay
        self.spikes = spikes
        self.out = out
        self.out_weights = out_weights

    @staticmethod
    def from_neuron_json(neuron_json: OrderedDict[str, Any]):
        id: str = neuron_json.get("id")
        position = Position.from_json(neuron_json.get("position"))
        is_input = bool(neuron_json.get("isInput") == "true")
        is_output = bool(neuron_json.get("isOutput") == "true")
        rules: RuleSet = RuleSet({}) if is_output or is_input else RuleSet(set(map(lambda rule_str: Rule.from_rule_str(rule_str), str(neuron_json.get("rules")).split(" "))))
        starting_spikes = int(neuron_json.get("startingSpikes") or 0)
        delay = int(neuron_json.get("delay") or 0)
        spikes = int(neuron_json.get("spikes") or 0)

        out: List[str] = [] if neuron_json.get("out") == None else ([*neuron_json.get("out")] if type(neuron_json.get("out")) == list else [neuron_json.get("out")])
        out_weights_str: OrderedDict[str, str] = neuron_json.get("outWeights") or {}
        out_weights: OrderedDict[str, int] =  {k: int(v) for k, v in out_weights_str.items()}

        return Neuron(id, position, is_input, is_output, rules, starting_spikes, delay, spikes, out, out_weights)

    @staticmethod
    def multiplier_neuron(neuron_prime: "Neuron", neuron: "Neuron", index: int):
        spikes_produced = {rule.release * neuron_prime.out_weights[neuron.id] for rule in neuron_prime.rules}

        return Neuron(
            id = f"{neuron_prime.id}-{neuron.id}-{index}",
            position = neuron_prime.position.get_translate(30 * index, 0),
            is_input = False,
            is_output = False,
            rules = RuleSet({Rule(
                rule_re = RuleRE({(spike_produced, StarExpSet({}), PlusExpSet({}))}), 
                consume = spike_produced, 
                release = spike_produced, 
                delay = 0, 
                ) for spike_produced in spikes_produced}),

            starting_spikes = 0,
            delay = 0,
            spikes = 0,
            out = [neuron.id],
            out_weights={neuron.id: 1}
        ), spikes_produced
        

    def translate(self, x: int):
        '''Note that this operation acts on the neuron itself'''
        self.spikes += x
        self.rules = RuleSet({rule.translate(x) for rule in self.rules})


    def scale(self, x: int):
        '''Note that this operation acts on the neuron itself'''
        self.spikes *= x
        self.rules = RuleSet({rule.scale(x) for rule in self.rules})


    def get_rules_xmp_str(self):
        rule_str_list: List[str] = []

        for rule in self.rules:
            rule_str_list.append(rule.to_xmp_str())
        
        return " ".join(rule_str_list)
        


    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Neuron):
            return self.id == __o.id
        
        return False
    
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self) -> str:
        return f"{self.id}"

    def __repr__(self) -> str:
        return self.__str__()