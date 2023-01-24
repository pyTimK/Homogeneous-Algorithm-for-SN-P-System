import json
import xmltodict
from collections import OrderedDict
from typing import Any, List
import re

def main():
    # input_json = load_xmp("test")
    # input_json = load_xmp("outtest")
    input_json = load_xmp("sub-homogeneous-register")
    snp_system = Snp_system(input_json)
    # save_json("fk", input_json)




def xmp_to_snp(input_xmp: OrderedDict[str, Any]):
    return 



class Snp_system:
    """
    Main class for SN P systems
    """
    def __init__(self, input_json: OrderedDict[str, Any]) -> None:
        self.neurons: List[Neuron]= []

        content_json = input_json["content"]
        neuron_ids = list(content_json.keys())

        for neuron_id in neuron_ids:
            neuron_json: OrderedDict[str, Any] = content_json[neuron_id]
            self.neurons.append(Neuron(neuron_json))


class Neuron:
    """
    Represents a neuron in an SN P system
    """
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

        



class Rule:
    """
    Represents a rule in a neuron of an SN P system
    """
    __symbol = "a"
    def __init__(self, rule_str: str) -> None:
        self.rule_str = rule_str
        # print(f">>>>>>>> {rule_str}")
        match = re.match(fr"(.*)/(\w+)->(\w*);(\w*)", rule_str)
        # print(match.groups())
        
        reg_exp_str, consume_str, release_str, delay_str = match.groups()

        self.reg_exp_bounded: List[int] = []
        self.reg_exp_star: List[int] = []
        self.reg_exp_plus: List[int] = []


        star_pattern = r"\((.*)\)\*"
        stars_str: List[str] = re.findall(star_pattern, reg_exp_str)
        reg_exp_str: str = re.sub(star_pattern, "", reg_exp_str)
        self.star: List[int] = [1 if x == "a" else int(x.replace("a", "")) for x in stars_str]

        plus_pattern = r"\((.*)\)\+"
        pluses_str: List[str] = re.findall(plus_pattern, reg_exp_str)
        reg_exp_str: str = re.sub(plus_pattern, "", reg_exp_str)
        self.plus: List[int] = [1 if x == "a" else int(x.replace("a", "")) for x in pluses_str]


        boundeds_str = reg_exp_str.split(Rule.__symbol)[:-1]
        self.bounded: List[int] = [1 if x == "" else int(x) for x in boundeds_str]


        self.consume = 1 if consume_str == "a" else int(consume_str.replace(Rule.__symbol, ""))

        if (release_str == "0"):
            self.release = 0
        elif (release_str == "a"):
            self.release = 1
        else:
            self.release = int(release_str.replace(Rule.__symbol, ""))

        self.delay = int(delay_str)

        # print(f"Regexp bounded: {self.bounded}")
        # print(f"Regexp star: {self.star}")
        # print(f"Regexp plus: {self.plus}")
        # print(f"Consume: {self.consume}")
        # print(f"Release: {self.release}")
        # print(f"Delay: {self.delay}")


class Position:
    """
    Contains the x and y coordinates of a neuron
    """
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_json(cls, position_json: OrderedDict[str, str]):
        return cls(float(position_json["x"]), float(position_json["y"]))







def load_xmp(name: str) -> OrderedDict[str, Any]:
    """
    Load the input file and convert from xmp to python dictionary
    """
    with open(f"{name}.xmp") as xmp_input_file:
        xmp_str = xmp_input_file.read()
        return xmltodict.parse(xmp_str)


def save_json(name: str, input: OrderedDict[str, Any]):
    """
    Save the json to a file
    """
    json_data = json.dumps(input)
    with open(f"{name}.json", "w") as json_file:
        json_file.write(json_data)



if __name__ == "__main__":
    main()