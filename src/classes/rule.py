
import re
from .period_constants_pair import PeriodConstantsPair
from .event import Event
from .rule_transition import RuleTransition
from src.errors.not_unbounded_error import NotUnboundedError
from typing import List, Set
from .constants import Constants
from copy import deepcopy

class Rule:
    """Represents a rule in a neuron of an SN P system"""

    __symbol = "a"
    __reg_exp_delimeter = "U"

    def __init__(self, period_constants_pair: PeriodConstantsPair, consume: int, release: int, delay: int) -> None:
        self.period_constants_pair = period_constants_pair
        self. consume = consume
        self.release = release
        self.delay = delay
        self.rule_transition = Rule.__get_rule_transition(period_constants_pair, consume, release, delay)


    @staticmethod
    def from_rule_str(rule_str: str):
        match = re.match(fr"(.*)/(\w+)->(\w*);(\w*)", rule_str)
        reg_exp_str, consume_str, release_str, delay_str = match.groups()

        period_constants_pair = Rule.__get_period_constants_pair(reg_exp_str)
        consume = Rule.__get_consume(consume_str)
        release = Rule.__get_release(release_str)
        delay = Rule.__get_delay(delay_str)

        return Rule(period_constants_pair, consume, release, delay)

    
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
            # if len(star_set) == 0:
            #     raise NotUnboundedError(0, reg_exp_str, unb_reg_exp)
            
            if len(star_set) > 1:
                raise NotUnboundedError(2, reg_exp_str, unb_reg_exp)


            # 3. the period would be the single element of the star set
            period = 0 if len(star_set) == 0 else star_set.pop()

            period_constants_pairs.append(PeriodConstantsPair(period, Constants({constant})))

        return PeriodConstantsPair.union(*period_constants_pairs)
    
    @staticmethod
    def __get_bounded_str(constant: int):
        if constant == 0:
            return ""
        
        if constant == 1:
            return Rule.__symbol
        
        return f"{constant}{Rule.__symbol}"

    @staticmethod
    def __get_star_str(period: int):
        if period == 0:
            return ""
        
        if period == 1:
            return f"({Rule.__symbol})*"
        
        return f"({period}{Rule.__symbol})*"

    @staticmethod
    def __get_reg_exp_str(pcp: PeriodConstantsPair):
        reg_exp_union: List[str] = []

        star_str = Rule.__get_star_str(pcp.period)
        for constant in pcp.constants:
            bounded_str = Rule.__get_bounded_str(constant)
            reg_exp_union.append(f"{bounded_str}{star_str}")
        
        return reg_exp_union

    @staticmethod
    def __get_consume(consume_str: str):
        if consume_str == Rule.__symbol:
            return 1

        return int(consume_str.replace(Rule.__symbol, ""))
    
    @staticmethod
    def __get_consume_str(consume: int) -> str:
        if consume == 1:
            return Rule.__symbol
        
        return f"{consume}{Rule.__symbol}"
    
    @staticmethod
    def __get_release(release_str: str):
        if release_str == "0":
            return 0

        if release_str == Rule.__symbol:
            return 1
        
        return int(release_str.replace(Rule.__symbol, ""))


    @staticmethod
    def __get_release_str(release: int) -> str:
        if release == 0:
            return "0"

        if release == 1:
            return Rule.__symbol
        
        return f"{release}{Rule.__symbol}"

    
    @staticmethod
    def __get_delay(delay_str: str):
        return int(delay_str)
    
    @staticmethod
    def __get_delay_str(delay: int) -> str:
        return str(delay)

    @staticmethod
    def __get_rule_transition(period_constants_pair: PeriodConstantsPair, consume: int, release: int, delay: int):
        return RuleTransition(period_constants_pair, Event(consume, release, delay))

    
    @staticmethod
    def from_rule_transition(rule_transition: RuleTransition):
        return Rule(rule_transition.state, rule_transition.event.alpha, rule_transition.event.beta.release, rule_transition.event.beta.delay)


    def to_xmp_str(self):
        reg_exp_union = Rule.__get_reg_exp_str(self.period_constants_pair)
        consume_str = Rule.__get_consume_str(self.consume)
        release_str = Rule.__get_release_str(self.release)
        delay_str = Rule.__get_delay_str(self.delay)

        rule_str_list: List[str] = []

        for reg_exp in reg_exp_union:
            rule_str = f"{reg_exp}/{consume_str}->;{release_str};{delay_str}"
            rule_str_list.append(rule_str)
        
        return " ".join(rule_str_list)

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
