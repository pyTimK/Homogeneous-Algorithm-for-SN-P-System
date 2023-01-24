import json
import xmltodict
from collections import OrderedDict
from typing import Any, List, Set, Tuple, Type, Self
import re
import math
from functools import reduce


def main():
    # input_json = load_xmp("outtest")
    input_json = load_xmp("test")
    # input_json = load_xmp("sub-homogeneous-register")
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
    __reg_exp_delimeter = "U"
    def __init__(self, rule_str: str) -> None:
        self.rule_str = rule_str
        # print(f">>>>>>>> {rule_str}")
        match = re.match(fr"(.*)/(\w+)->(\w*);(\w*)", rule_str)
        # print(match.groups())
        
        reg_exp_str, consume_str, release_str, delay_str = match.groups()

        unb_reg_exp_list: List[str] = reg_exp_str.split(Rule.__reg_exp_delimeter)

        period_constants_pairs: List[PeriodConstantsPair] = []

        for unb_reg_exp in unb_reg_exp_list:
            #! star Set
            star_pattern = r"\((.*)\)\*"
            stars_str: List[str] = re.findall(star_pattern, unb_reg_exp)
            unb_reg_exp: str = re.sub(star_pattern, "", unb_reg_exp)
            star_set: Set[int] = {1 if x == "a" else int(x.replace("a", "")) for x in stars_str}

            #! plus List
            plus_pattern = r"\((.*)\)\+"
            pluses_str: List[str] = re.findall(plus_pattern, unb_reg_exp)
            unb_reg_exp: str = re.sub(plus_pattern, "", unb_reg_exp)
            plus_list: List[int] = [1 if x == "a" else int(x.replace("a", "")) for x in pluses_str]


            #! bounded List
            boundeds_str = unb_reg_exp.split(Rule.__symbol)[:-1]
            bounded_list: List[int] = [1 if x == "" else int(x) for x in boundeds_str]


            #! period-constants pair (p, Q)
            # 1. Convert plus to star and add the constant to the bounded list
            for plus in plus_list:
                star_set.add(plus)
                bounded_list.append(plus)
            
            # 2. The constant will be the sum of all bounded ints
            constant = sum(bounded_list)

            # Note that the star_set must contain a single element,
            # else the input is invalid and the algorithm cannot proceed
            if len(star_set) == 0:
                raise NotUnboundedError(0, reg_exp_str, unb_reg_exp)
            
            elif len(star_set) > 1:
                raise NotUnboundedError(2, reg_exp_str, unb_reg_exp)


            # 3. the period would be the single element of the star set
            period = star_set.pop()

            period_constants_pairs.append(PeriodConstantsPair(period, {constant}))
        
        self.period_constants_pair = PeriodConstantsPair.combine(period_constants_pairs)
        # print(self.period_constants_pair)




        #! consume
        self.consume = 1 if consume_str == "a" else int(consume_str.replace(Rule.__symbol, ""))


        #! release
        if (release_str == "0"):
            self.release = 0
        elif (release_str == "a"):
            self.release = 1
        else:
            self.release = int(release_str.replace(Rule.__symbol, ""))


        #! delay
        self.delay = int(delay_str)

        # print(f"Regexp bounded: {self.bounded}")
        # print(f"Regexp star: {self.star}")
        # print(f"Regexp plus: {self.plus}")
        # print(f"Consume: {self.consume}")
        # print(f"Release: {self.release}")
        # print(f"Delay: {self.delay}")

class NotUnboundedError(Exception):
    """Raised when the input is not a finite union of unbounded regular expressions"""
    def __init__(self, type: int, reg_exp: str, unb_reg_exp: str):
        if (type == 0):
            message = "The algorithm does not work on bounded regular expressions in the form a^i"
        else:
            message = "The algorithm does not work on regular expressions with multiple stars, e.g., \"(2a)*(3a)*\""

        self.message = f"{message}\nThe error was found on \"{unb_reg_exp}\" part of the regular expression \"{reg_exp}\""

    def __str__(self):
        return self.message

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


class PeriodConstantsPair:
    def __init__(self, period: int, constants: Set[int]) -> None:
        self.period = period
        self.constants = constants

    @staticmethod
    def combine(period_constants_pairs: List["PeriodConstantsPair"]):
        if len(period_constants_pairs) == 0:
            raise ValueError("Called \"combine\" with no item in period_constant_pairs list")

        return reduce(PeriodConstantsPair.__combine_two, period_constants_pairs)

    def __combine_two(pcp1: "PeriodConstantsPair", pcp2: "PeriodConstantsPair"):
        p, q, p_prime, q_prime = pcp1.period, pcp1.constants, pcp2.period, pcp2.constants
        l = MyMath.lcm(p, p_prime)
        q_bar: Set[int] = set()
        q_bar_prime: Set[int] = set()
        for p_mult in range(0, l - p + 1, p):
            for q_item in q:
                q_bar.add(q_item + p_mult)

        for p_prime_mult in range(0, l - p_prime + 1, p_prime):
            for q_prime_item in q_prime:
                q_bar_prime.add(q_prime_item + p_prime_mult)
        
        return PeriodConstantsPair(l, q_bar.union(q_bar_prime))
    

    def __str__(self) -> str:
        return f"Period: {self.period}\tConstants: {self.constants}"
                


class MyMath:
    @staticmethod
    def lcm(a: int, b: int):
        return (a*b)//math.gcd(a,b)


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