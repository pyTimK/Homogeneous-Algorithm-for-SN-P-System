from collections import OrderedDict
from .rule import Rule
from .position import Position
from typing import Any, List

class Neuron:
    """Represents a neuron in an SN P system"""

    def __init__(self, neuron_json: OrderedDict[str, Any]) -> None:
        self.id: str = neuron_json.get("id")
        self.position = Position.from_json(neuron_json.get("position"))
        self.is_input = neuron_json.get("isInput") == "true"
        self.is_output = neuron_json.get("isOutput") == "true"

        self.rules = [] if self.is_output or self.is_input else list(map(lambda rule_str: Rule(rule_str), str(neuron_json.get("rules")).split(" ")))
        self.starting_spikes = int(neuron_json.get("startingSpikes") or 0)
        self.delay = int(neuron_json.get("delay") or 0)
        self.spikes = int(neuron_json.get("spikes") or 0)
        
        self.out: List[str] = [] if neuron_json.get("out") == None else [*neuron_json.get("out")]
        out_weights_str: OrderedDict[str, str] = neuron_json.get("outWeights") or {}
        self.out_weights =  {k: int(v) for k, v in out_weights_str.items()}