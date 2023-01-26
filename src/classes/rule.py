
import re
from .period_constants_pair import PeriodConstantsPair
from .event import Event
from .rule_transition import RuleTransition
from src.errors.not_unbounded_error import NotUnboundedError
from typing import List, Set

class Rule:
    """Represents a rule in a neuron of an SN P system"""

    __symbol = "a"
    __reg_exp_delimeter = "U"


    def __init__(self, rule_str: str) -> None:
        self.rule_str = rule_str

        match = re.match(fr"(.*)/(\w+)->(\w*);(\w*)", rule_str)
        reg_exp_str, consume_str, release_str, delay_str = match.groups()

        #! Period-constants pair (p, Q)
        self.period_constants_pair = Rule.__get_period_constants_pair(reg_exp_str)

        #! Consume
        self.consume = Rule.__get_consume(consume_str)

        #! Release
        self.release = Rule.__get_release(release_str)

        #! Delay
        self.delay = Rule.__get_delay(delay_str)

        #! Rule Transition Representation
        self.rule_transition = RuleTransition(self.period_constants_pair, Event(self.consume, self.release, self.delay))

    
    @staticmethod
    def __get_period_constants_pair(reg_exp_str: str):
        unb_reg_exp_list: List[str] = reg_exp_str.split(Rule.__reg_exp_delimeter)

        period_constants_pairs: List[PeriodConstantsPair] = []

        for unb_reg_exp in unb_reg_exp_list:
            #? Star Set
            star_pattern = r"\((.*)\)\*"
            stars_str: List[str] = re.findall(star_pattern, unb_reg_exp)
            unb_reg_exp: str = re.sub(star_pattern, "", unb_reg_exp)
            star_set: Set[int] = {1 if x == "a" else int(x.replace("a", "")) for x in stars_str}

            #? Plus List
            plus_pattern = r"\((.*)\)\+"
            pluses_str: List[str] = re.findall(plus_pattern, unb_reg_exp)
            unb_reg_exp: str = re.sub(plus_pattern, "", unb_reg_exp)
            plus_list: List[int] = [1 if x == "a" else int(x.replace("a", "")) for x in pluses_str]


            #? Bounded List
            boundeds_str = unb_reg_exp.split(Rule.__symbol)[:-1]
            bounded_list: List[int] = [1 if x == "" else int(x) for x in boundeds_str]


            #? Removing all the plus
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
        
        return PeriodConstantsPair.union(*period_constants_pairs)

    @staticmethod
    def __get_consume(consume_str: str):
        return 1 if consume_str == "a" else int(consume_str.replace(Rule.__symbol, ""))
    
    @staticmethod
    def __get_release(release_str: str):
        if (release_str == "0"):
            return 0

        if (release_str == "a"):
            return 1
        
        return int(release_str.replace(Rule.__symbol, ""))
    
    @staticmethod
    def __get_delay(delay_str: str):
        return int(delay_str)


    def __str__(self) -> str:
        return str(self.rule_transition)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Rule):
            return self.period_constants_pair == __o.period_constants_pair and self.consume == __o.consume and self.release == __o.release and self.delay == __o.delay
        
        return False
    
    def __hash__(self):
        return hash((self.period_constants_pair, self.consume, self.release, self.delay))
